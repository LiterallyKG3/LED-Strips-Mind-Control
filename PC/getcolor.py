import mss
import numpy as np
from PIL import Image

def getcolor(method="mean", resize=(200, 200)):
    # method: 'mean', 'median', 'dominant'
    # resize: scale down to increase speed, up to increase accuracy

    with mss.mss() as sct:
        # grab monitor screenshot and resize
        monitor = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
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
            b = int(np.median(arr[:,:,2]))
            return r, g, b

        elif method == "dominant":
            palette_img = im.convert('P', palette=Image.ADAPTIVE, colors=8)
            palette = palette_img.getpalette()
            color_counts = palette_img.getcolors()
            dominant_color_index = max(color_counts, key=lambda item: item[0])[1]
            r = palette[dominant_color_index * 3]
            g = palette[dominant_color_index * 3 + 1]
            b = palette[dominant_color_index * 3 + 2]
            return r, g, b
        else:
            raise ValueError("Invalid method, supported methods: 'mean', 'median', or 'dominant'")