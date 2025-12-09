from machine import Pin
from ir_rx.nec import NEC_8 # Change to desired protocol
import time

# CONFIG #
IR_PIN = 28 # IR Receiver DATA GPIO Pin

# receive IR code
def callback(data, addr):
    if data < 0:
        return
    print("Received code:", hex(data), " addr:", hex(addr))

ir = NEC_8(Pin(IR_PIN, Pin.IN), callback)

while True:
    time.sleep(0.01)