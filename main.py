from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import os
import random
from server import start_server
import webbrowser
import requests
import socket

def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
local_ip = get_ip()

api_port = random.randint(3000, 9000)


def create_image(width, height, color1, color2):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image

def connect_callback(icon, item):
    webbrowser.open_new_tab(f"http://localhost:{api_port}/connect")


def quit_callback(icon, item):
    requests.get(f"http://localhost:{api_port}/shutdown")
    exit()


# In order for the icon to be , you must provide an icon
icon = Icon('test', create_image(20, 20, "black", "white"), menu=Menu(
    MenuItem(
        'Connect',
        connect_callback,
    ),
))
start_server(port=api_port, ip=local_ip)
icon.run()

# To finally show you icon, call run
