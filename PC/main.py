import time
import requests
import sendrgb
import getcolor

retryDelay = 1
updateInterval = 0.05

while True:
    try:
        r, g, b = getcolor.getcolor()
        print("RGB: ", r, g, b)
        sendrgb.sendrgb(r, g, b)

    except requests.exceptions.RequestException as e:
        print("Error sending to Pi:", e)
        print(f"Retrying in {retryDelay} seconds...")
        time.sleep(retryDelay)
        continue

    time.sleep(updateInterval)