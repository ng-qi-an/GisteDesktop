import requests
from utils import os_system, get_version
from clint.textui import progress
import os
DOWNLOAD_URL="https://gistedownloadmanager.popqa17.repl.co"
request = requests.get(DOWNLOAD_URL)
data = request.json()
if data['version'] == get_version():
    print("Giste is up to date!")
    if os_system == 'win32':
        print('Running Giste')
        os.system("Giste.exe")
        os._exit(0)
    elif os_system == 'darwin':
        pass
else:
    print('Update is available!')
    if os_system == 'win32':
        print('== Installing Update ==')
        if os.path.exists("Giste.exe"):
            os.remove("Giste.exe")
        r = requests.get(f"{DOWNLOAD_URL}/upgrade/{data['version']}", stream=True)
        with open("Giste.exe", 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                if chunk:
                    f.write(chunk)
                    f.flush()
        print("!= Update successfully installed =!")
        with open(f"version.txt", "w") as f:
            f.write(data['version'])
        print('Running Giste')
        os.system("Giste.exe")
        os._exit(0)
    elif os_system == 'darwin':
        print('Reinstall Giste via Git to get the latest updates.')

        