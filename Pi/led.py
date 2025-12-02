from machine import Pin
import uasyncio as asyncio

led = Pin("LED", Pin.OUT)

led_state = "startup"

async def led_manager():
    global led_state

    while True:

        if led_state == "startup":
            led.toggle()
            await asyncio.sleep(2)

        elif led_state == "wifi_connecting":
            led.on()
            await asyncio.sleep(0.2)
            led.off()
            await asyncio.sleep(0.2)

        elif led_state == "wifi_connected":
            led.on()
            await asyncio.sleep(1)
            led.off()
            await asyncio.sleep(1)

        elif led_state == "server_ready":
            for _ in range(2):
                led.on()
                await asyncio.sleep(0.5)
                led.off()
                await asyncio.sleep(0.5)
            await asyncio.sleep(3)
            
        elif led_state == "ir_transmitting":
            for _ in range(2):
                led.on()
                await asyncio.sleep(0.1)
                led.off()
                await asyncio.sleep(0.1)
            await asyncio.sleep(1)
            
        elif led_state == "error":
            led.on()
            await asyncio.sleep(0.05)
            led.off()
            await asyncio.sleep(0.05)

        else:
            # fallback
            led.off()
            await asyncio.sleep(0.5)