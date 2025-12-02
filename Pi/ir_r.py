from machine import Pin
from ir_rx.nec import NEC_8
import time

IR_PIN = 28

def callback(data, addr, ctrl):
    if data < 0:
        return
    print("Received code:", hex(data), " addr:", hex(addr))

ir = NEC_8(Pin(IR_PIN, Pin.IN), callback)

while True:
    time.sleep(0.01)