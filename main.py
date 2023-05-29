from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import os
from server import start_server
import webbrowser
from utils import documents_path, get_ip, toast



local_ip = get_ip()

api_port = 12436

# if not os.path.exists(f'{documents_path}/GisteData'):
#     os.makedirs(f'{documents_path}/GisteData')
#     make_ssl()

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
    webbrowser.open_new_tab(f"http://{local_ip}:{api_port}/connect")


def quit_callback(icon, item):
    os._exit(1)


# In order for the icon to be , you must provide an icon
icon = Icon('test', create_image(20, 20, "black", "white"), menu=Menu(
    MenuItem(
        'Connect',
        connect_callback,
    ),
    MenuItem(
        'Quit',
        quit_callback,
    ),
))

toast("GisteDesktop Started", "GisteDesktop has been started. Click here to connect.", f"http://{local_ip}:{api_port}/connect")

start_server(port=api_port, ip=local_ip)
icon.run()

# To finally show you icon, call run
