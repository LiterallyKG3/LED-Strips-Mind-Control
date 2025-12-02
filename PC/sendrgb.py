import requests

def sendrgb(r, g, b):
    
    pico_ip = "http://ENTERPICOIPHERE"

    rgb = f"{r},{g},{b}"

    response = requests.get(f"{pico_ip}/?rgb={rgb}")
    print("Server response:", response.text)