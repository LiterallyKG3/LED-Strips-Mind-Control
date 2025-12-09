import asyncio
import sendrgb
import getcolor
import os
import sys

UPDATE_INTERVAL = 0.05

# console theme & header
COLOR = "\033[38;5;208m"
BOLD = "\033[1m"
RESET = "\033[0m"
RGB_FMT = COLOR + "RGB:" + RESET + " " + BOLD + "{} {} {}" + RESET

def header():
    if os.name == "nt":
        print(f"\033]0;LED-Strips-Mind-Control\007", end="", flush=True)
    if os.name != "nt":
        print("\33]0;LED-Strips-Mind-Control\a", end="", flush=True)


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

            print(RGB_FMT.format(r, g, b))

            await sendrgb.udp(r, g, b)

            last_rgb = (r, g, b)

        await asyncio.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n" + BOLD + COLOR + "Exiting..." + RESET)
        sys.exit(0)
