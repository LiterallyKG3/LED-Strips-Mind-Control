import asyncio
import sendrgb
import getcolor
import os

UPDATE_INTERVAL = 0.05

# console theme & header
COLOR = "\033[38;5;208m"
BOLD = "\033[1m"
RESET = "\033[0m"

def header():
    os.system("title LED-Strips-Mind-Control")

    print()
    print(BOLD + COLOR + "==== INITIATING PACKAGE DELIVERY ====" + RESET)
    print()

# main
async def main():

    header()

    asyncio.create_task(sendrgb.discover_pico())

    last_rgb = None

    while True:

        r, g, b = getcolor.getcolor()

        if last_rgb != (r, g, b):

            print(COLOR + "RGB:" + RESET, f"{BOLD}{r} {g} {b}{RESET}")

            await sendrgb.udp(r, g, b)

            last_rgb = (r, g, b)

        await asyncio.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
