<div align="center">

# [ LED STRIPS MIND CONTROL ]

</div>
  
<p align="center">
  <img src="/assets/demo.gif" width="800">
</p>
  
<h2 align="center">
    Turns any generic IR-controlled LED Strip into ambient lighting syncing with the monitor's average color every <ins>~100 milliseconds</ins> using a Microcontroller and an IR Transmitter module
</h2>
<br><br><br><br><br><br><br><br><br>


# How it works
PC takes a screenshot using **mss** and resizes it with **Pillow** (200x200 by default), then converts the image to a single RGB value using **NumPy** with 3 selectable methods: `mean`, `median` or `dominant` (default: `mean`).  

The RGB value is sent over to a Raspberry Pi Pico W via Wi-Fi.
The Pi calculates which of the strip's 20 preset color is the closest match (or turns it OFF if image is near black), and blasts the corresponding IR frequencies to the LED Strip.

Before this, the IR frequencies for each button on the strip’s remote were recorded (see `IR_codes.md`). These can be remapped easily if your strip uses a different IR protocol. 

```mermaid
graph LR;
    PC-->Pi;
    Pi-->LED;
```
<br><br><br>


# Features
- Selectable RGB grabbing methods
- UDP (default) & HTTP (fallback) communication between PC and Pi
- Automatic IP Broadcast and discovery
- Customizable IR transmit values
- Smooth fade transitions between colors
- LED Strip Brightness Control
- LED States on the Raspberry Pi Pico W
<br><br><br>


# Requirements
### Hardware
- PC
- Raspberry Pi Pico W (doesn't matter if it's the second one)
- IR Transmitter Module
- IR Receiver Module (For learning your remote)
- Generic IR-controlled LED Strip (NEC-8 protocol in this repo, but easily replaceable)
- LED Strip Remote
- Duct Tape (Optional)

### Software
- Python 3.12+
- IDE for PC Client (VScode works)
- Thonny or mpremote
- MicroPython firmware for the Pico W
- Windows (Linux not supported yet)
- Python Packages:
  - `pillow`
  - `numpy`
  - `mss`
<br><br><br>


# Setup
### 1. Flash MicroPython to your Pico W  
Download the latest `.uf2` from:  
https://micropython.org/download/rp2-pico-w/  

Then drag and drop onto the Pico's USB drive.  

### 2. Upload IR Libraries and Pi Scripts
Using Thonny or mpremote, upload everything inside the repo's `Pi/` folder:
- lib/
- ir_r.py
- ir_t.py
- led.py
- main.py
- server.py
- wifi.py
  
The Pico's root directory should now look like:  
```
/  
├── lib  
├── ir_r.py  
├── ir_t.py  
├── led.py  
├── main.py  
├── server.py  
└── wifi.py
```

Reboot the Pico when done.

### 3. Configure Pico Wi-Fi
Using Thonny or mpremote, edit `wifi.py` and add your Wi-Fi name and password:  

```
SSID = "ENTERSSIDHERE"  
PASSWORD = "ENTERPASSWORDHERE"  
```

Save the file.
The PC will automatically detect the Pico via UDP broadcast.  

### 4. Wire the IR Receiver to the Pico
Recommended wiring:  

```
Pin 36 (3V3 OUT) → VCC    
Pin 38 (GND) → GND  
Pin 34 (GP28) → DATA or IN  
```

You can find the Pico W Pinout Diagram [here.](https://datasheets.raspberrypi.com/picow/PicoW-A4-Pinout.pdf)

### 5. Record your LED Remote's IR Codes
Using Thonny or mpremote, run the `ir_r` script and press the buttons on your LED remote pointing it at the receiver. 

>[!NOTE]
> If your strip doesn't use NEC-8, change `from ir_rx.nec import NEC_8` in `ir_r` to the protocol your LED Strip uses.

Take the captured codes and replace the existing ones in `ir_t.py`.

### 6. Install PC dependencies
Open a terminal and run:  

`pip install numpy pillow mss`  

### 7. Wire the IR Transmitter Module
Recommended wiring:

```
Pin 36 (3V3 OUT) → VCC  
Pin 38 (GND) → GND  
Pin 34 (GP28) → DATA or IN  
```

You can find the Pico W Pinout Diagram [here.](https://datasheets.raspberrypi.com/picow/PicoW-A4-Pinout.pdf)

Make sure the transmitter points at the LED Strip's IR receiver.

### 8. Power the Pico
Connect USB. The Pico will boot and wait for incoming RGB values.

### 9. Run the PC client
Download everything inside the repo's `PC/` folder.  

Open the directory in your IDE and run `main.py`.  

The PC will detect the Pico on LAN and start sending RGB values.  

The Pico will translate them into IR signals and control the LED Strip.
<br><br><br>


# Credits
[IR Libraries](https://github.com/peterhinch/micropython_ir)  
[NumPy](https://numpy.org)   
[Pillow](https://pypi.org/project/pillow/)  
[mss](https://pypi.org/project/mss/)
