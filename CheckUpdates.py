import requests
from versioning import GISTE_DESKTOP
from utils import os_system

request = requests.get("https://gistedownloadmanager.popqa17.repl.co")
data = request.json()
if data['version'] == GISTE_DESKTOP:
    print("Giste is up to date!")
    if os_system == 'win32':
        # run Giste.exe in program files
        pass
    elif os_system == 'darwin':
        pass
else:
    print('UPDATE AVAILABLE')
    if os_system == 'win32':
        # run auto updater
        pass
    elif os_system == 'darwin':
        print('Reinstall Giste via Git to get the latest updates.')

        