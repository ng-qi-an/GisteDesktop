import subprocess
# Generate MacOS .app files

fpackages = []

# requirements = open("requirements.txt", "r")
# for package in requirements.readlines():
#     fpackages.append(package.replace("\n", ""))

# print(fpackages)

try:
    subprocess.run(["python3", "setup.py", "py2app", "-A"])
except Exception as e:
    raise e