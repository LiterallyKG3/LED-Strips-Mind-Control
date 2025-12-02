import mss
import numpy as np
from PIL import Image

def getcolor():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        im = Image.frombytes('RGB', sct_img.size, sct_img.rgb).resize((50,50))
        arr = np.array(im)
        r = int(arr[:,:,0].mean())
        g = int(arr[:,:,1].mean())
        b = int(arr[:,:,2].mean())
        return r, g, b