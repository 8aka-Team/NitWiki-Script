import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
import platform

if platform.system() == 'Windows':
    os.system("pip install rtoml-0.10.0-cp311-none-win_amd64.whl ")
else:
    os.system("pip install rtoml")

os.system("python3 -m pip install pyyaml tqdm psutil requests imageio rtoml elevate colorama nuitka ordered-set")

if os.path.exists("dist"):
    shutil.rmtree("dist")

os.mkdir("build")
os.mkdir("dist")


def build(file):
    filepath = os.path.join(os.getcwd(), "src", file)
    print(f"build {file}", flush=True)
    args = ["python", "-m", "nuitka", "--onefile", filepath, "--assume-yes-for-downloads", "--output-dir=build"]
    if platform.system() == 'Windows':
        args.append("--windows-icon-from-ico=favicon.png")
        args.append("--enable-plugins=upx")
        args.append("--upx-binary=upx.exe")
    if platform.system() == 'MacOS':
        args.append("--macos-app-icon=favicon.png")
    if platform.system() == 'Linux':
        args.append("--linux-icon=favicon.png")
    subprocess.call(args)
    filename = os.path.splitext(file)[0]
    for f in os.listdir(os.path.join(os.getcwd(), "build")):
        if f.startswith(filename) and not os.path.isdir(os.path.join(os.getcwd(), "build", f)):
            shutil.move(os.path.join(os.getcwd(), "build", f), os.path.join(os.getcwd(), "dist", f))


for file in os.listdir(os.path.join(os.getcwd(), "src")):
    if file != "utils.py":
        build(file)

# 傻逼
# 狗屎代碼
