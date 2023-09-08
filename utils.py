import base64
import os
import socket
import sys

os_system = sys.platform

if os_system == "darwin":
    import pync
if os_system == "win32":
    import win11toast

def encode_base64(message):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode('ascii')


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

def toast(title, text, onClick=None):
    if os_system == 'win32':
        win11toast.notify(title, text, on_click=onClick)
    elif os_system == 'darwin':
        pync.notify(text, title=title, open=onClick)
        
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
