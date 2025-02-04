import os.path
from concurrent.futures import ThreadPoolExecutor, wait
from utils import *

script_license()

pool = ThreadPoolExecutor(6)
task = []


def download_task(name: str, url: str):
    def _download():
        print(f"开始下载{name}")
        try:
            download(url, os.path.join(os.getcwd(), "plugins", name + ".jar"))
        except Exception as e:
            print(f"下载错误{e},在下载{name}")
            print("重试")
            _download()
        else:
            print(f"下载完成{name}")

    task.append(pool.submit(_download))


def downloads():
    # 下载各个插件
    download_task("ProtocolLib", "https://ci.dmulloy2.net/job/ProtocolLib/lastSuccessfulBuild/artifact/build/libs"
                                 "/ProtocolLib.jar")
    download_task("Luckperms", "https://download.luckperms.net/1570/bukkit/loader/LuckPerms-Bukkit-5.4.153.jar")
    download_task("PlaceholderAPI",
                  "https://ci.extendedclip.com/job/PlaceholderAPI/200/artifact/build/libs/PlaceholderAPI-2.11.7-DEV-200.jar")
    download_task("PlugManx", "https://github.com/Test-Account666/PlugManX/releases/download/2.4.1/PlugManX-2.4.1.jar")
    download_task("FastAsyncWorldEdit",
                  "https://github.com/IntellectualSites/FastAsyncWorldEdit/releases/download/2.12.3/FastAsyncWorldEdit-Paper-2.12.3.jar")
    download_task("EssentialsX", "https://dl.8aka.org/plugins/EssentialsX-2.21.0-dev%2B110-f1a5caf.jar")
    download_task("Multiverse-Core",
                  "https://cdn.modrinth.com/data/3wmN97b8/versions/jbQopAkk/multiverse-core-4.3.14.jar")
    download_task("AuthMe", "https://cdn.modrinth.com/data/3IEZ9vol/versions/oezVemzR/AuthMe-5.7.0-FORK-Universal.jar")
    download_task("SkinRestorer", "https://ci.codemc.io/job/SkinsRestorer/job/SkinsRestorer/lastSuccessfulBuild"
                                  "/artifact/build/libs/SkinsRestorer.jar")
    download_task("MiniMotd", "https://cdn.modrinth.com/data/16vhQOQN/versions/SgOOeke0/minimotd-bukkit-2.1.5.jar")
    download_task("TrChat", "https://github.com/TrPlugins/TrChat/releases/download/v2.1.3/TrChat-2.1.3.jar")
    download_task("PacketEvents",
                  "https://cdn.modrinth.com/data/HYKaKraK/versions/qsiAokbs/packetevents-spigot-2.7.0.jar")


if __name__ == "__main__":
    if not os.path.exists("plugins"):
        os.mkdir("plugins")
    downloads()
    wait(task)
    print("完成！")
    exit_()
