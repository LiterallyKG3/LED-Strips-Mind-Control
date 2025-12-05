import led
from wifi import wlan
import uasyncio as asyncio

last_rgb = None

async def handle_client(reader, writer):
    
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
    

async def start_server():
    
    while not wlan.isconnected():
        print("Server waiting for Wi-Fi...")
        led.led_state = "wifi_connecting"
        await asyncio.sleep(1)
    
    while True:
        try:
            print("Server starting...")
            server = await asyncio.start_server(handle_client, "0.0.0.0", 80)
            print("Server running!")
            led.led_state = "server_ready"
            
            while wlan.isconnected():
                await asyncio.sleep(1)
                
            print("Wi-Fi disconnected. Closing server...")
            led.led_state = "server_closed"
            server.close()
            await server.wait_closed()
            await asyncio.sleep(1)
            
        except Exception as e:
            print("Server error:", e)
            led.led_state = "error"
            await asyncio.sleep(2)