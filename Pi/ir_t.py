from machine import Pin
from ir_tx.nec import NEC
import server
import led
from time import ticks_ms, ticks_diff
import uasyncio as asyncio

# CONFIG
IR_PIN = 28
NEC_ADDR = 0x00
SEND_COOLDOWN = 0.1
FUNCTION_SLEEPS = 0.12
FADE_STEPS = 3
FADE_MIN_SLEEP = 0.08
BRIGHTNESS_SMOOTHING = 0.2
BRIGHT_DEBOUNCE = 0.25

nec = NEC(Pin(IR_PIN, Pin.OUT))

# IR codes
IR_ON = 0x40
IR_OFF = 0x41

BRIGHT_25 = 0x17
BRIGHT_50 = 0x13
BRIGHT_75 = 0xf
BRIGHT_100 = 0xb

IR_MAP = {
    0x58: (255, 0, 0), # R0
    0x54: (255, 63, 0), # R1
    0x50: (255, 126, 0), # R2
    0x1c: (255, 189, 0), # R3
    0x18: (255, 255, 0), # R4
    0x59: (0, 255, 0), # G0
    0x55: (0, 255, 63), # G1
    0x51: (0, 255, 126), # G2
    0x1d: (0, 255, 189), # G3
    0x19: (0, 255, 255), # G4
    0x45: (0, 0, 255), # B0
    0x49: (63, 0, 255), # B1
    0x4d: (126, 0, 255), # B2
    0x1e: (189, 0, 255), # B3
    0x1a: (255, 0, 255), # B4
    0x44: (255, 255, 255), # W0
    0x48: (215, 190, 255), # W1
    0x4c: (185, 135, 255), # W2
    0x1f: (176, 184, 255), # W3
    0x1b: (43, 202, 255), # W4
}

# states
last_send = ticks_ms() - int(SEND_COOLDOWN * 1000)
current_rgb = (0, 0, 0)
current_ir_code = None
strip_on = False
current_brightness_level = 4 # 1..4 (25%..100%)
last_brightness_send = ticks_ms() - int(BRIGHT_DEBOUNCE * 1000)
send_lock = asyncio.Lock()

# brightness management
def rgb_luminance(rgb):
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def luminance_to_level(lum): # 1..4
    if lum < 18:
        return 0
    elif lum < 60:
        return 1
    elif lum < 130:
        return 2
    elif lum < 200:
        return 3
    else:
        return 4
    
def level_to_code(level):
    if level == 1:
        return BRIGHT_25
    elif level == 2:
        return BRIGHT_50
    elif level == 3:
        return BRIGHT_75
    elif level == 4:
        return BRIGHT_100
    else:
        return None

# find nearest color
def nearest_color(rgb):
    r1, g1, b1 = rgb
    best_code = None
    best_dist = 10**12
    
    for code, (r2, g2, b2) in IR_MAP.items():
        dist = (r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2
        if dist < best_dist:
            best_dist = dist
            best_code = code
    # debug print
    # print("RGB", rgb , "matched to code", best_code , "with distance", best_dist)
    return best_code

# send IR code
async def send(code):
    global last_send

    cooldown_ms = int(SEND_COOLDOWN * 1000)
    async with send_lock:
        now = ticks_ms()
        elapsed = ticks_diff(now, last_send)
        if elapsed < cooldown_ms:
            await asyncio.sleep((cooldown_ms - elapsed) / 1000)
        
    try:
        print("Sending IR:", hex(code))
        nec.transmit(NEC_ADDR, code)
        led.led_state = "ir_transmitting"
        last_send = ticks_ms()
    except Exception as e:
        print("IR transmit error:", e)
        led.led_state = "error"
    await asyncio.sleep(FUNCTION_SLEEPS)
        
# ensure ON before sending color
async def ensure_on():
    global strip_on

    if strip_on:
        return
    await send(IR_ON)
    await asyncio.sleep(FUNCTION_SLEEPS)
    strip_on = True
    
# ensure off
async def ensure_off():
    global strip_on

    if not strip_on:
        return
    await send(IR_OFF)
    await asyncio.sleep(FUNCTION_SLEEPS)
    strip_on = False

# step fade between colors
async def fade_to_color(code):
    global current_rgb, current_ir_code
    
    if code == current_ir_code:
        return
    
    r1, g1, b1 = current_rgb
    r2, g2, b2 = IR_MAP[code]

    for i in range(1, FADE_STEPS + 1):
        t = i / FADE_STEPS
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        
        if i == FADE_STEPS:
            await send(code)
            
        await asyncio.sleep(FADE_MIN_SLEEP)
        
    current_rgb = (r2, g2, b2)
    current_ir_code = code
    
# send brightness
async def send_brightness(level):
    global current_brightness_level, last_brightness_send
    
    if level == 0:
        await ensure_off()
        current_brightness_level = 0
        return
    
    if level == current_brightness_level:
        return
    
    now = ticks_ms()
    debounce_ms = int(BRIGHT_DEBOUNCE * 1000)
    
    if ticks_diff(now, last_brightness_send) < debounce_ms:
        return
    
    code = level_to_code(level)
    if code is not None:
        await ensure_on()
        await send(code)
        current_brightness_level = level
        last_brightness_send = ticks_ms()
        await asyncio.sleep(FUNCTION_SLEEPS)
    
# update color with brightness smoothing
async def update_color(target_rgb):
    global current_rgb

    # brightness smoothing
    r = current_rgb[0] + (target_rgb[0] - current_rgb[0]) * BRIGHTNESS_SMOOTHING
    g = current_rgb[1] + (target_rgb[1] - current_rgb[1]) * BRIGHTNESS_SMOOTHING
    b = current_rgb[2] + (target_rgb[2] - current_rgb[2]) * BRIGHTNESS_SMOOTHING

    smoothed = (int(r), int(g), int(b))
    current_rgb = smoothed
    
    # brightness handling
    lum = rgb_luminance(smoothed)
    level = luminance_to_level(lum)
    await send_brightness(level)
    
    if level == 0:
        return

    await ensure_on()
    code = nearest_color(smoothed)
    if code is not None:
        await fade_to_color(code)


# main loop
async def main():
    
    print("IR Transmitter ready")

    while True:
        rgb = server.last_rgb
        if rgb is not None:
            try:
                await update_color(rgb)
            except Exception as e:
                print("IR loop error:", e)
                led.led_state = "error"
        await asyncio.sleep(0.02)