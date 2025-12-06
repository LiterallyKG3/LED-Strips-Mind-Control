# import requests # HTTP fallback
import socket
import asyncio

BROADCAST_PORT = 5005
UDP_PORT = 6006
DISCOVERY_INTERVAL = 1
RETRY_DELAY = 0.05

pico_ip = None
last_sent_rgb = None

send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
send_sock.setblocking(False)

discovery_sock = None

async def discover_pico():
    global pico_ip, discovery_sock

    if discovery_sock is None:
        discovery_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        discovery_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        discovery_sock.bind(('', BROADCAST_PORT))
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
        await asyncio.sleep(0.01)

        await asyncio.sleep(DISCOVERY_INTERVAL)

async def udp(r, g, b):
    global pico_ip, last_sent_rgb

    if not pico_ip:
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
        await asyncio.sleep(RETRY_DELAY)

'''
# HTTP fallback
async def http(r, g, b):

    rgb = f"{r},{g},{b}"

    response = requests.get(f"{pico_ip}/?rgb={rgb}")
    print("Server response:", response.text)
'''
