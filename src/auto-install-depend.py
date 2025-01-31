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
    download_task("Luckperms", "https://ci.lucko.me/job/LuckPerms/1549/artifact/bukkit/loader/build/libs/LuckPerms"
                               "-Bukkit-5.4.134.jar")
    download_task("PlaceholderAPI", "https://ci.extendedclip.com/job/PlaceholderAPI/193/artifact/build/libs"
                                    "/PlaceholderAPI-2.11.6-DEV-193.jar")
    download_task("PlugManx", "https://github.com/Test-Account666/PlugManX/releases/download/2.4.0/PlugManX-2.4.0.jar")
    download_task("WorldEdit", "https://ci.enginehub.org/repository/download/bt10/23766:id/worldedit-bukkit-7.3.1"
                               "-SNAPSHOT-dist.jar?branch=version/7.3.x&guest=1")
    download_task("EssentialsX", "https://dl.8aka.org/plugins/EssentialsX-2.21.0-dev%2B110-f1a5caf.jar")
    download_task("Multiverse-Core", "https://ci.onarandombox.com/job/Multiverse-Core/870/artifact/target/Multiverse"
                                     "-Core-4.3.2-SNAPSHOT.jar")
    download_task("AuthMe", "https://cdn.modrinth.com/data/3IEZ9vol/versions/oezVemzR/AuthMe-5.7.0-FORK-Universal.jar")
    if not os.path.exists("plugins/spark"):
        download_task("spark",
                      "https://ci.lucko.me/job/spark/410/artifact/spark-bukkit/build/libs/spark-1.10.65-bukkit.jar")
    download_task("SkinRestorer", "https://ci.codemc.io/job/SkinsRestorer/job/SkinsRestorer/lastSuccessfulBuild"
                                  "/artifact/build/libs/SkinsRestorer.jar")
    download_task("MiniMotd", "https://cdn.modrinth.com/data/16vhQOQN/versions/MXvCSw18/minimotd-bukkit-2.1.0.jar")
    download_task("TrChat", "https://github.com/TrPlugins/TrChat/releases/download/v2.1.0/TrChat-2.1.0.jar")


if __name__ == "__main__":
    if not os.path.exists("plugins"):
        os.mkdir("plugins")
    downloads()
    wait(task)
    print("完成！")
    exit_()
