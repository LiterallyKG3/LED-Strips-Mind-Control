import asyncio
import sendrgb
import getcolor

UPDATE_INTERVAL = 0.01

async def main():
        asyncio.create_task(sendrgb.discover_pico())

        last_rgb = None
        while True:
                r, g, b = await getcolor.getcolor()

                if last_rgb != (r, g, b):
                        print("RGB:", r, g, b)
                        await sendrgb.udp(r, g, b)
                        # await sendrgb.http(r, g, b) # http fallback
                        last_rgb = (r, g, b)

                await asyncio.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())