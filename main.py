from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import os
from server import start_server
import webbrowser
from utils import get_ip, toast, resource_path



local_ip = get_ip()
api_port = 12436

# == callbacks for menu items ==
def connect_callback(icon, item):
    webbrowser.open_new_tab(f"http://{local_ip}:{api_port}/host")


def quit_callback(icon, item):
    os._exit(1)

icon = Icon('test', Image.open(resource_path("giste.png")), menu=Menu(
    MenuItem(
        'Connect',
        connect_callback,
    ),
    MenuItem(
        'Quit',
        quit_callback,
    ),
))

# show a notification
toast("GisteDesktop Started", "GisteDesktop has been started. Click here to connect.", f"http://{local_ip}:{api_port}/host")

# start the API server
start_server(port=api_port, ip=local_ip)

# Add the icon to the menubar (macOS) or system tray (windows).
icon.run()

