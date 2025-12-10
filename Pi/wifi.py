import network
import time
import led
import uasyncio as asyncio

# CONFIG #
SSID = "ENTERSSIDHERE"           # Wi-Fi Name
PASSWORD = "ENTERPASSWORDHERE"   # Wi-Fi Password
CHECK_INTERVAL = 5               # Wi-Fi monitor check interval (seconds)
CONNECTION_TIMEOUT = 120         # Wi-Fi connection timeout (seconds)

wlan = network.WLAN(network.STA_IF) # create Wi-Fi station

# connect to Wi-Fi
async def connect():
    wlan.active(True) # enable Wi-Fi radio
    
    # already connected
    if wlan.isconnected():
        print("Already connected :D IP:", wlan.ifconfig()[0])
        led.led_state = "wifi_connected"
        return
    
    # connect
    print("Connecting to Wi-Fi...")
    wlan.connect(SSID, PASSWORD)
    led.led_state = "wifi_connecting"

    # timeout
    start = time.time()
    while not wlan.isconnected():
        if time.time() - start > CONNECTION_TIMEOUT:
            print("Failed to connect within timeout.")
            led.led_state = "error"
            return
        await asyncio.sleep(1)
        
    await asyncio.sleep(0.3) # DHCP stabilization sleep
    
    print("Connected :3 IP:", wlan.ifconfig()[0])
    led.led_state = "wifi_connected"

# monitor Wi-Fi connection and reconnect if lost
async def monitor():
    while True:
        if not wlan.isconnected():
            print("Wi-Fi disconnected. Reconnecting...")
            led.led_state = "wifi_connecting"
            await connect()
        await asyncio.sleep(CHECK_INTERVAL)