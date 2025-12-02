import network
import time
import led
import uasyncio as asyncio

SSID = "test"
PASSWORD = "WASD1414"
checkInterval = 5
connectionTimeout = 120

wlan = network.WLAN(network.STA_IF) # create station


async def connect():
    wlan.active(True) # enable Wi-Fi radio
    
    if wlan.isconnected():
        print("Already connected :D IP:", wlan.ifconfig()[0])
        led.led_state = "wifi_connected"
        return
    
    wlan.connect(SSID, PASSWORD)
    start = time.time()
    
    while not wlan.isconnected():
        if time.time() - start > connectionTimeout:
            print("Failed to connect within timeout.")
            led.led_state = "error"
            return
        
        print("Connecting to Wi-Fi...")
        led.led_state = "wifi_connecting"
        await asyncio.sleep(1)
            
        print("Connected :3 IP:", wlan.ifconfig()[0])
        led.led_state = "wifi_connected"


async def monitor():
    while True:
        if not wlan.isconnected():
            print("Wi-Fi disconnected. Attempting reconnection...")
            await connect()
            led.led_state = "error"
        await asyncio.sleep(checkInterval)