import led
import socket
from wifi import wlan
import uasyncio as asyncio

# CONFIG #
UDP_PORT = 6006          # UDP RGB Receive port
BROADCAST_PORT = 5005    # UDP IP Broadcast port

last_rgb = None

# Broadcast IP to PC via UDP
async def broadcast_ip():
    while not wlan.isconnected():
        await asyncio.sleep(1)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    ip = wlan.ifconfig()[0]
    print("Broadcasting IP...")
    
    while True:
        try:
            s.sendto(ip.encode(), ('255.255.255.255', BROADCAST_PORT))
            await asyncio.sleep(1)
        except Exception as e:
            print("IP Broadcast error:", e)
            led.led_state = "error"
            await asyncio.sleep(1)

# Receive RGB values with UDP
async def udp():
    global last_rgb
    
    while not wlan.isconnected():
        print("Server waiting for Wi-Fi...")
        led.led_state = "wifi_connecting"
        await asyncio.sleep(5)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', UDP_PORT))
    s.setblocking(False)
    print("Server Running!")
    led.led_state = "server_running"
        
    while True:
        try:
            data, addr = s.recvfrom(1024)
            r, g, b = map(int, data.decode().split(","))
            if last_rgb != (r, g, b):
                last_rgb = (r, g, b)
                print("Received RGB:", last_rgb)
        except OSError:
            await asyncio.sleep(0.005)
        except Exception as e:
            print("Server error:", e)
            led.led_state = "error"
            await asyncio.sleep(0.1)

'''
# HTTP server fallback
# uncomment this block, and:
# in Pi/main.py, Replace:
# asyncio.create_task(server.udp())
# with:
# asyncio.create_task(server.run_http_server())
# to use.
# Also see HTTP server fallback in PC/sendrgb.py

async def http(reader, writer):
    global last_rgb
    
    try:
        request = await reader.read(1024)
        if not request:
            await writer.aclose()
            return 
        
        request = request.decode()

        if "rgb=" in request:
            try:
                raw = request.split("rgb=")[1].split(" ")[0]
                r, g, b = raw.split(",")
                last_rgb = (int(r), int(g), int(b))
                print("Received RGB:", last_rgb)
            except Exception as e:
                print("Failed to parse RGB.", e)
                led.led_state = "error"
                
        # send response
        response = ("HTTP/1.1 200 Hello\r\nContent-Type: text/plain\r\n\r\nHello".encode())
        await writer.awrite(response)
        
    except Exception as e:
        print("Client Error:", e)
        led.led_state = "error"
        
    await writer.aclose()

async def run_http_server():
    server = await asyncio.start_server(http, "0.0.0.0", 80)
    print("Server running!")
    led.led_state = "server_ready"
    await server.wait_closed
'''