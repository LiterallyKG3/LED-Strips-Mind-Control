<div align="center">

# [ LED STRIPS MIND CONTROL ]

</div>
  
<p align="center">
  <img src="/images/demo.gif" width="800">
</p>
  
<h2 align="center">
    Turns any generic IR-controlled LED Strip into ambient lighting syncing with the monitor's average color every <ins>~100 milliseconds</ins> using a Microcontroller and an IR Transmitter module
</h2>
<br><br><br><br><br><br>


# How it works
PC takes a screenshot using **mss** and resizes it with **Pillow** (200x200 by default), then converts the image to a single RGB value using **NumPy** with 3 selectable methods: `mean`, `median` or `dominant` (default: `mean`).  

The RGB value is sent over to a Raspberry Pi Pico W via Wi-Fi.
The Pi calculates which of the strip's 20 preset colors (remappable) is the closest match (or turns the strip OFF if image is near black), and blasts the corresponding IR frequencies to the LED Strip.

Before this, the IR frequencies for each button on the strip’s remote were recorded (see `IR_codes.md`). These can be remapped easily if your strip uses a different IR protocol. 

```mermaid
graph LR;
    PC-->Pi;
    Pi-->LED;
```


# Features
- Selectable RGB grabbing methods
- UDP (default) & HTTP (fallback) communication between PC and Pi
- Automatic IP Broadcast and discovery
- Customizable IR transmit values
- Smooth fade transitions between colors
- Brightness Control
- LED States on the Raspberry Pi Pico W
<br><br><br><br><br><br>


# Requirements
### Hardware
- PC
- Raspberry Pi Pico W (doesn't matter if it's the second one) **with pin headers soldered**
- IR Transmitter Module (3.3V)
- IR Receiver Module (For learning your remote)
- Jumper Wires (For connecting the modules)
- Generic IR-controlled LED Strip (NEC-8 protocol in this repo, but easily replaceable)
- LED Strip Remote
<br><br>

### Software
- Python 3.12+
- IDE for PC Client (VScode works)
- Thonny or mpremote
- MicroPython firmware for the Pico W
- Windows or Linux
- Python Packages:
  - `pillow`
  - `numpy`
  - `mss`
<br><br><br>


# Setup
### 1. Flash MicroPython to your Pico W  
Download the latest `.uf2` from:  
https://micropython.org/download/rp2-pico-w/  
<br>
Then drag and drop onto the Pico's USB drive.
<br><br><br><br>

### 2. Upload IR Libraries and Pi Scripts
Using Thonny or mpremote, upload everything inside the repo's `Pi/` folder to the Pico.
<br><br>

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
<br><br><br><br>

### 3. Configure Pico Wi-Fi
Using Thonny or mpremote, edit `wifi.py` and add your Wi-Fi name and password:  

```
SSID = "ENTERSSIDHERE"  
PASSWORD = "ENTERPASSWORDHERE"  
```
<br>

Save the file.
<br><br>
The PC will automatically detect the Pico via UDP broadcast.
<br><br>

>[!IMPORTANT]
> The Pico has to be connected to the same Wi-Fi network as your PC.

<br><br><br><br>

### 4. Wire the IR Receiver to the Pico
Recommended wiring:  

```
Pin 36 (3V3 OUT) → VCC    
Pin 38 (GND) → GND  
Pin 34 (GP28) → DATA or IN  
```

> [!WARNING]
> You'll need to change `IR_PIN` in `ir_r` if you connect DATA to another GPIO pin
<br>

You can find the Pico W Pinout Diagram [here.](https://datasheets.raspberrypi.com/picow/PicoW-A4-Pinout.pdf)
<br><br><br><br>

### 5. Record your LED Remote's IR Codes
Using Thonny or mpremote, run the `ir_r` script and press the buttons on your LED remote pointing it at the receiver. 

>[!NOTE]
> If your strip doesn't use NEC-8, change `from ir_rx.nec import NEC_8` in `ir_r` to the protocol your LED Strip uses.
<br>

Take the captured codes and replace the existing ones in `ir_t.py` and then save the file.
<br><br><br><br>

### 6. Wire the IR Transmitter Module
Recommended wiring:

```
Pin 36 (3V3 OUT) → VCC  
Pin 38 (GND) → GND  
Pin 34 (GP28) → DATA or IN  
```

> [!WARNING]
> You'll need to change `IR_PIN` in `ir_t` if you connect DATA to another GPIO pin
<br>

You can find the Pico W Pinout Diagram [here.](https://datasheets.raspberrypi.com/picow/PicoW-A4-Pinout.pdf)  
<br>

Make sure the transmitter points at the LED Strip's IR receiver.
<br><br><br><br>

### 7. Power the Pico
Connect USB. The Pico will boot and wait for incoming RGB values.
<br><br><br><br>



### 8. Install PC dependencies
Open a terminal and run:  

`pip install numpy pillow mss`
<br><br><br><br>

### 9. Run the PC client
Download everything inside the repo's `PC/` folder.  

Open the directory in your IDE and run `main.py`.  
<br>

>[!NOTE]
> Make sure to allow Python through your firewall so the PC client can communicate with the Pico over your network.

<br>

The PC will detect the Pico on LAN and start sending RGB values.  

The Pico will translate them into IR signals and control the LED Strip.
<br><br><br><br>


# Credits
[IR Libraries](https://github.com/peterhinch/micropython_ir)  
[NumPy](https://numpy.org)   
[Pillow](https://pypi.org/project/pillow/)  
[mss](https://pypi.org/project/mss/)
