import asyncio
import mss
import numpy as np
from PIL import Image
from collections import Counter

def getcolor(method="mean", resize=(200, 200)):
    # method: 'mean', 'median', 'dominant'
    # resize: scale down to increase speed, up to increase accuracy

    with mss.mss() as sct:
        # grab monitor screenshot and resize
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        im = Image.frombytes('RGB', sct_img.size, sct_img.rgb).resize((resize))
        arr = np.array(im)

        if method == "mean":
            r = int(arr[:,:,0].mean())
            g = int(arr[:,:,1].mean())
            b = int(arr[:,:,2].mean())
            return r, g, b
        
        elif method == "median":
            r = int(np.median(arr[:,:,0]))
            g = int(np.median(arr[:,:,1]))
            b = int(np.median(arr[:,:,1]))
            return r, g, b

        elif method == "dominant":
            pixels = arr.reshape(-1, 3)
            pixels_tuples = [tuple(p) for p in pixels]
            most_common = Counter(pixels_tuples).most_common(1)[0][0]
            r, g, b = most_common
            return r, g, b
        else:
            raise ValueError("Invalid method, supported methods: 'mean', 'median', or 'dominant'")