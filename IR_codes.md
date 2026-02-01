## Command, IRcode, RGB

# Tested NEC_8 Remote & LED (NEC_ADDR = 0x00)
### Colors
- R0, 0x58, (255, 0, 0)
- R1, 0x54, (255, 63, 0)
- R2, 0x50, (255, 126, 0)
- R3, 0x1c, (255, 189, 0)
- R4, 0x18, (255, 255, 0)

- G0, 0x59, (0, 255, 0)
- G1, 0x55, (0, 255, 63)
- G2, 0x51, (0, 255, 126)
- G3, 0x1d, (0, 255, 189)
- G4, 0x19, (0, 255, 255)

- B0, 0x45, (0, 0, 255)
- B1, 0x49, (63, 0, 255)
- B2, 0x4d, (126, 0, 255)
- B3, 0x1e, (189, 0, 255)
- B4, 0x1a, (255, 0, 255)

- W0, 0x44, (255, 255, 255)
- W1, 0x48, (215, 190, 255)
- W2, 0x4c, (185, 135, 255)
- W3, 0x1f, (176, 184, 255)
- W4, 0x1b, (43, 202, 255)

### OFF/ON
- OFF, 0x41
- ON, 0x40  

### Brightness
- BRT DOWN, 0x5d
- BRT UP, 0x5c
- BRT 25%, 0x17
- BRT 50%, 0x13
- BRT 75%, 0xf
- BRT 100%, 0xb  

### Built-in LED Strip animation commands
- JUMP3, 0x15
- JUMP7, 0x11
- FADE3, 0xd
- FADE7, 0x9
- AUTO, 0xe
- FLASH, 0xa  

- QUICK, 0x16
- SLOW, 0x12

<p align="left">
  <img src="/images/remote_NEC8.png" width="400">
</p>

# Tested NEC_16 Remote & LED (NEC_ADDR = 0xef00)
### Colors
- R0, 0x4, (255, 0, 0)
- R1, 0x8, (255, 160, 0)
- R2, 0xc, (160, 255, 0)
- R3, 0x10, (110, 255, 0)

- G0, 0x5, (0, 255, 0)
- G1, 0x9, (0, 255, 160)
- G2, 0xd, (0, 160, 255)
- G3, 0x11, (0, 110, 255)

- B0, 0x6, (0, 0, 255)
- B1, 0xa, (110, 0, 255)
- B2, 0xe, (160, 0, 255)
- B3, 0x12, (200, 0, 255)

- W0, 0x7, (255, 255, 255)

### OFF/ON
- OFF, 0x2
- ON, 0x3

### Brightness
- BRT DOWN, 0x1
- BRT UP, 0x0

### Built-in LED Strip animation commands
- FLASH, 0xb
- STROBE, 0xf
- FADE, 0x13
- SMOOTH, 0x17

<p align="left">
  <img src="/images/remote_NEC16.png" width="400">
</p>
