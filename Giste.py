import pyautogui
import webbrowser
import sys
import os
from git import Repo

giste_dir = os.path.expanduser('~/Library/Application Support/GisteDesktop')


if sys.platform == 'win32':
     os_prefix = "py"
elif sys.platform == 'darwin':
    os_prefix = "python3"

try:
    os.system(f"{os_prefix} --version")
except:
    if pyautogui.alert(text='Oops! It seems like python hasn\'t been installed yet. Click OK to download.', title='Third-Party installations', button='OK') == 'OK':
        webbrowser.open("https://www.python.org/downloads/")
        exit(1)

try:
    os.system("git")
except:
    if pyautogui.alert(text='Git has not been downloaded yet! Click OK to download.', title='Third-Party installations', button='OK') == 'OK':
        webbrowser.open("https://git-scm.com/downloads")
        exit(1)

while True:
    if os.path.exists(giste_dir):
        repo = Repo(f"{giste_dir}/.git")
        if repo.commit().hexsha != repo.remotes.origin.fetch()[0].commit.hexsha:
            print("pulling")
            Repo(f"{giste_dir}/.git").remotes.origin.pull()
        os.system(f'{os_prefix} "{giste_dir}/main.py"')
        exit(1)
    else:
        Repo.clone_from("https://github.com/ng-qi-an/GisteDesktop.git", giste_dir)
