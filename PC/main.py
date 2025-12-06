import asyncio
import sendrgb
import getcolor
import os

UPDATE_INTERVAL = 0.01

# console theme
GREEN = "\033[32m"
BOLD = "\033[1m"
RESET = "\033[0m"

def header():
    os.system("title LED-Strips-Mind-Control")

    print(BOLD + GREEN + "==== INITIATING PACKAGE DELIVERY ====" + RESET)
    print()

async def main():
    
    header()

    asyncio.create_task(sendrgb.discover_pico())

    last_rgb = None

    while True:
        r, g, b = await getcolor.getcolor()

        if last_rgb != (r, g, b):
            print(
                GREEN + "RGB:" + RESET,
                f"{BOLD}{r} {g} {b}{RESET}"
            )

            await sendrgb.udp(r, g, b)
            # await sendrgb.http(r, g, b) # http fallback

            last_rgb = (r, g, b)

        await asyncio.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
