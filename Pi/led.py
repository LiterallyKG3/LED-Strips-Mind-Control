from machine import Pin
import uasyncio as asyncio

led = Pin("LED", Pin.OUT)

led_state = "startup"

# Pi LED states
async def led_manager():
    global led_state

    while True:
        s = led_state

        if s == "startup":
            led.toggle()
            await asyncio.sleep(2)

        elif s == "wifi_connecting":
            led.on()
            await asyncio.sleep(0.2)
            led.off()
            await asyncio.sleep(0.2)

        elif s == "wifi_connected":
            led.on()
            await asyncio.sleep(1)
            led.off()
            await asyncio.sleep(2)

        elif s == "server_ready":
            for _ in range(2):
                led.on()
                await asyncio.sleep(0.5)
                led.off()
                await asyncio.sleep(0.5)
            await asyncio.sleep(3)
            
        elif s == "ir_transmitting":
            for _ in range(2):
                led.on()
                await asyncio.sleep(0.1)
                led.off()
                await asyncio.sleep(0.1)
            await asyncio.sleep(1)
            
        elif s == "error":
            led.on()
            await asyncio.sleep(0.01)
            led.off()
            await asyncio.sleep(0.01)

        else:
            # fallback
            led.toggle()
            await asyncio.sleep(0.1)