import network
import time
import led
import uasyncio as asyncio

SSID = "ENTERSSIDHERE"
PASSWORD = "ENTERPASSWORDHERE"
checkInterval = 5
connectionTimeout = 120

wlan = network.WLAN(network.STA_IF) # create station
ip = wlan.ifconfig()[0]


async def connect():
    wlan.active(True) # enable Wi-Fi radio
    
    if wlan.isconnected():
        if ip != "0.0.0.0":
            print("Already connected :D IP:", ip)
            led.led_state = "wifi_connected"
            return
    
    print("Connecting to Wi-Fi...")
    wlan.connect(SSID, PASSWORD)
    led.led_state = "wifi_connecting"
    start = time.time()
    
    while not wlan.isconnected():
        if time.time() - start > connectionTimeout:
            print("Failed to connect within timeout.")
            led.led_state = "error"
            return
        await asyncio.sleep(1)
        
    await asyncio.sleep(0.5)
    print("Connected :3 IP:", ip)
    led.led_state = "wifi_connected"


async def monitor():
    while True:
        if not wlan.isconnected() or ip == "0.0.0.0":
            print("Wi-Fi disconnected. Attempting reconnection...")
            led.led_state = "error"
            await connect()
        await asyncio.sleep(checkInterval)