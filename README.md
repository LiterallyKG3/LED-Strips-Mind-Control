## Turns any generic IR-controlled LED strip into ambient lights syncing with the monitor's mean color every ~50 milliseconds using a Microcontroller and an IR Transmitter module.


PC takes a screenshot using mss, converts the mean color to a single RGB value using NumPy (firstly resizes the image for faster calculation with Pillow), sends them over to my Raspberry Pi Pico 2 W via Wi-Fi, The Pi calculates which of the 20 colors my LED strip has is the closest (or OFF if color is close to black and also factors in brightness), and blasts the corresponding IR frequencies to the LED strip.

I first had to record the IR frequencies for each of the buttons my strip's remote has (mine uses the NEC-8 protocol) and map them to an approximate range of RGB based on the actual color the LED outputs.  
  
  
  
Credit:  
[IR Libraries](https://github.com/peterhinch/micropython_ir)   
[NumPy](https://numpy.org)  
[Pillow](https://pypi.org/project/pillow/)  
[mss](https://pypi.org/project/mss/)
