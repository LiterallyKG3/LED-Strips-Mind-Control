# import requests # HTTP fallback
import socket
import asyncio

# CONFIG #
DISCOVERY_PORT = 5005     # Pico discovery UDP port
UDP_PORT = 6006           # RGB send UDP port
DISCOVERY_INTERVAL = 1    # Pico discovery interval (seconds)
RETRY_DELAY = 0.05        # RGB send error retry delay (seconds) (0.05=50ms)

pico_ip = None
last_sent_rgb = None

# RGB send UDP socket
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
send_sock.setblocking(False)

# discover Pico via UDP broadcast
discovery_sock = None

async def discover_pico():
    global pico_ip, discovery_sock

    if discovery_sock is None:
        discovery_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        discovery_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        discovery_sock.bind(('', DISCOVERY_PORT))
        discovery_sock.setblocking(False)

    while True:
        try:
            data, addr = discovery_sock.recvfrom(1024)
            new_ip = data.decode()
            if new_ip != pico_ip:
                pico_ip = new_ip
                print("Discovered Pico IP:", pico_ip)
        except BlockingIOError:
            pass
        except Exception as e:
            print("Discovery error:", e)
        await asyncio.sleep(DISCOVERY_INTERVAL)

# send RGB with UDP
async def udp(r, g, b):
    global pico_ip, last_sent_rgb

    if not pico_ip:
        print("Pico IP not discovered yet")
        return

    rgb_tuple = (r, g, b)
    if rgb_tuple == last_sent_rgb:
        return
    
    rgb_bytes = f"{r},{g},{b}".encode()
    try:
        send_sock.sendto(rgb_bytes, (pico_ip, UDP_PORT))
        print("Package sent")
        last_sent_rgb = rgb_tuple
    except OSError as e:
        print("Error sending RGB:", e)
        print("Rediscovering Pico IP...")
        pico_ip = None
        await asyncio.sleep(RETRY_DELAY)

'''
# HTTP fallback
# uncomment this block, and:
# In PC/main.py, Replace:
# await sendrgb.udp(r, g, b)
# with:
# await sendrgb.http(r, g, b)
# at the top of PC/sendrgb.py, uncomment:
# # import requests # HTTP fallback
# to use.
# Also see HTTP server fallback in Pi/server.py

async def http(r, g, b):

    rgb = f"{r},{g},{b}"

    response = requests.get(f"{pico_ip}/?rgb={rgb}")
    print("Server response:", response.text)
'''
