import led
import wifi
import server
import ir_t
import uasyncio as asyncio
    
async def main():
    asyncio.create_task(led.led_manager())
    asyncio.create_task(wifi.connect())
    asyncio.create_task(wifi.monitor())
    asyncio.create_task(server.broadcast_ip())
    asyncio.create_task(server.udp())
    # asyncio.create_task(server.http()) # http fallback
    asyncio.create_task(ir_t.main())
    
    while True:
        await asyncio.sleep(1)

asyncio.run(main())