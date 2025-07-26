import os
import sys
import requests
import tqdm
import yaml
import traceback
from yaml import CLoader as Loader
import warnings
import colorama

warnings.filterwarnings("ignore")
colorama.init(autoreset=True)


def script_license():
    print("\033[92mMinecraft笨蛋脚本\033[0m")
    print("\033[92m作者:8aka-Team\033[0m")
    print("\033[92m仓库地址:https://github.com/8aka-Team/NitWiki-Script\033[0m")
    print("\033[91m未经许可,禁止用于商业用途\033[0m")
    


def handler(filename, loader=lambda fp: yaml.load(fp, Loader=Loader), dumper=yaml.dump):
    def a(func):
        def b(*args, **kwargs):
            print(f"开始配置{filename}")
            if not os.path.exists(filename):
                print(f"{filename}不存在,跳过")
                return
            try:
                with open(filename, 'r+', encoding="utf8") as fp:
                    config = loader(fp)

                func(config, *args, **kwargs)
                with open(filename, 'w+', encoding="utf8") as fp:
                    dumper(config, fp)
            except Exception as e:
                print(f"错误:{e}")
            else:
                print(f"完成配置{filename}")

        return b

    return a


def ask(title):
    YELLOW = '\033[33m'
    RESET = '\033[0m'
    title = f"{YELLOW}{title}{RESET}"
    select = input(f"{title}(y/n): ")
    if select.lower().startswith("y"):
        return True
    return False


def exit_():
    print("回车退出")
    input()
    sys.exit(0)


class ServerPropLoader:
    @staticmethod
    def load(fp):
        data = {}
        for line in fp.readlines():
            if not line.startswith("#"):
                k, v = line.split("=", 1)
                data[k] = v.strip()
        return data

    @staticmethod
    def dump(data, fp):
        for k, v in data.items():
            fp.write(k + "=" + str(v) + "\n")


def download(url, local_filepath):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/111.0.0.0 Safari/537.36"
    }
    try:
        with requests.get(url, stream=True, headers=headers, allow_redirects=True) as r:
            r.raise_for_status()
            size = int(r.headers["Content-Length"])
            chunk_size = 8192
            with tqdm.tqdm(
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    miniters=1,
                    desc=f"下载文件 {local_filepath}",
                    total=size,
            ) as pbar:
                with open(local_filepath, "wb") as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        f.write(chunk)
                        pbar.update(len(chunk))
    except Exception as e:
        print(f"下载错误:{e}")


def exception_hook(exc_type, exc_value, tb):
    print("\033[91m笨蛋脚本出现异常!!!\033[0m")
    traceback.print_exception(exc_type, exc_value, tb)
    exit_()


sys.excepthook = exception_hook
