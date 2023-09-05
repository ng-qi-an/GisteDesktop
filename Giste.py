import pyautogui
import webbrowser
import sys
import os
import subprocess
from git import Repo

giste_dir = os.path.expanduser('~/Library/Application Support/GisteDesktop')


if sys.platform == 'win32':
     os_prefix = "py"
elif sys.platform == 'darwin':
    os_prefix = "python3"


try:
    subprocess.run([f"{os_prefix}", "--version"])
except Exception as e:
    if pyautogui.alert(text='Oops! It seems like python hasn\'t been installed yet. Click OK to download.', title='Third-Party installations', button='OK') == 'OK':
        webbrowser.open("https://www.python.org/downloads/")
        raise e



try:
    subprocess.run("git")
except Exception as e:
    if pyautogui.alert(text='Git has not been downloaded yet! Click OK to download.', title='Third-Party installations', button='OK') == 'OK':
        webbrowser.open("https://git-scm.com/downloads")
        raise e



while True:
    if os.path.exists(giste_dir):
        repo = Repo(f"{giste_dir}/.git")
        if repo.commit().hexsha != repo.remotes.origin.fetch()[0].commit.hexsha:
            try:
                Repo(f"{giste_dir}/.git").remotes.origin.pull()
            except Exception as e:
                pyautogui.alert(text='An error occured with updating GisteDesktop. GisteDesktop will continue with outdated version.', title='Update Error', button='OK')
                print(e)
        try:
            # subprocess.run([f'{os_prefix}', f"{giste_dir}/main.py"])
            os.system(f'{os_prefix} "{giste_dir}/main.py"')

            exit(1)
        except Exception as e:
            pyautogui.alert(text=e, title='Application Error', button='OK')
            print(e)
    else:
        Repo.clone_from("https://github.com/ng-qi-an/GisteDesktop.git", giste_dir)
        # try:
        #     subprocess.run([f'{os_prefix}', '-m', 'pip', "install", '-r', f'{giste_dir}/requirements.txt'])
        # except Exception as e:
        #     pyautogui.alert(text=e, title='Package Installation Error', button='OK')
        #     print(e)
