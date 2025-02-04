import zipfile
from textwrap import dedent as _
from utils import *
from psutil import virtual_memory
import platform
import subprocess

script_license()
print("此向导将会自动为你生成启动脚本!")


def detect_jar():
    for i in os.listdir(os.getcwd()):
        if not os.path.isdir(i) and i.endswith(".jar"):
            print("找到服务端核心" + f"\033[32m{i}\033[0m!!\n")
            return i
    print("没有发现服务端核心,请将此脚本和服务端核心放在同一目录下再使用\n")
    return


class VersionMeta:
    pufferfish: bool = False
    leaf: bool = False
    minecraft_version: int = 0


def detect_brand(jar_path):
    meta = VersionMeta()
    with zipfile.ZipFile(jar_path, 'r') as jar:
        if 'META-INF/versions.list' in jar.namelist():
            manifest_data = jar.read('META-INF/versions.list').decode('utf-8')
            a = manifest_data.split('\t')
            meta.version = int(a[1].split('.')[1])
            brand = a[2].split('/')[1].split('-')[0].lower()
            if brand == 'leaf':
                meta.leaf = True
            if brand in ["pufferfish", "purpur", "leaves", "gale", "leaf"]:
                meta.pufferfish = True
    return meta


def ask(title):
    while True:
        select = input(title + "(y/n):")
        if select.lower().startswith("y"):
            print()
            return True
        elif select.lower().startswith("n"):
            print()
            return False
        else:
            print("\033[31m输入错误,请输入 y 或者 n\033[0m\n")


def get_memory():
    return int(virtual_memory().available / (1024 * 1024))  # to MB


def get_java(path, check):
    try:
        result = subprocess.run([path, "-version"], capture_output=True, text=True)
        print("成功检测到java!版本为:")
        print(result.stderr)
        return True

    except FileNotFoundError or subprocess.CalledProcessError:
        if check:
            print("\033[31m警告,找不到java,请重新指定java路径,或者不自行指定java!\033[0m\n")
        else:
            print("\033[31m警告,找不到java,请检查java环境变量或手动指定java路径!\033[0m\n")

        return False


def generate_command(server: str, meta: VersionMeta):
    while True:
        if ask("自行指定 java 路径?"):
            java = input("请输入 java 路径(应当以 java.exe 结尾, 如 D:/jdk/bin/java.exe):")
            if get_java(java, True):
                java = '"' + java + '"'
                break
        else:
            if get_java("java", False):
                java = "java"
                break

    if ask("自动检测使用内存?"):
        memory = get_memory() - 1000  # to MB
        if memory / 1024 > 20:
            memory = 20 * 1024
        print(f"\033[32m自动使用内存{memory}MB\033[0m\n")
    else:
        memory = int(input("内存(至少1024MB,不建议为服务器分配少于2048MB的内存)(单位为MB,输入时不带单位):"))
        if memory / 1024 > 20:
            print("不建议为您的服务器分配超过 16-20GB 的内存,给 Java 太多的内存可能会损害服务器的性能")

    if not ask("使用优化参数(推荐使用)?"):
        return f"{java} -Xms{memory}M -Xmx{memory}M -jar {server}"

    base = (
        f"{java} -Xms1024M -Xmx{memory}M -XX:+UnlockExperimentalVMOptions -XX:+UnlockDiagnosticVMOptions -XX:+UseFMA "
        f"-XX:+UseVectorCmov -XX:+UseNewLongLShift -XX:+UseFastStosb -XX:+SegmentedCodeCache "
        f"-XX:+OptimizeStringConcat -XX:+DoEscapeAnalysis -XX:+OmitStackTraceInFastThrow "
        f"-XX:+AlwaysActAsServerClassMachine -XX:+AlwaysPreTouch -XX:+DisableExplicitGC "
        f"-XX:NmethodSweepActivity=1 -XX:ReservedCodeCacheSize=400M -XX:NonNMethodCodeHeapSize=12M "
        f"-XX:ProfiledCodeHeapSize=194M -XX:NonProfiledCodeHeapSize=194M -XX:-DontCompileHugeMethods "
        f"-XX:MaxNodeLimit=240000 -XX:NodeLimitFudgeFactor=8000 -XX:+UseVectorCmov -XX:+PerfDisableSharedMem "
        f"-XX:+UseFastUnorderedTimeStamps -XX:+UseCriticalJavaThreadPriority -XX:ThreadPriorityPolicy=1 "
        f"-XX:AllocatePrefetchStyle=3 -XX:+UseG1GC -XX:MaxGCPauseMillis=37 -XX:+PerfDisableSharedMem "
        f"-XX:G1HeapRegionSize=16M -XX:G1NewSizePercent=23 -XX:G1ReservePercent=20 -XX:SurvivorRatio=32 "
        f"-XX:G1MixedGCCountTarget=3 -XX:G1HeapWastePercent=20 -XX:InitiatingHeapOccupancyPercent=10 "
        f"-XX:G1RSetUpdatingPauseTimePercent=0 -XX:MaxTenuringThreshold=1 "
        f"-XX:G1SATBBufferEnqueueingThresholdPercent=30 -XX:G1ConcMarkStepDurationMillis=5.0 -XX:GCTimeRatio=99 "
        f"-XX:G1ConcRefinementServiceIntervalMillis=150 -XX:G1ConcRSHotCardLimit=16 ")

    if meta.pufferfish and meta.minecraft_version >= 18:
        base += "--add-modules=jdk.incubator.vector "

    if meta.leaf:
        base += "-DLeaf.library-download-repo=https://maven.aliyun.com/repository/public "

    base += f"-jar {server} "

    if ask("关闭服务端自带GUI(GUI没啥用)(推荐关闭)"):
        base += "--nogui"

    return base


def generate_batch(command, restart):
    os_name = platform.system()
    if os_name == "Windows":
        with open("start.bat", "w", encoding="utf8") as fp:
            if restart:
                fp.write(_(f"""
                    @echo off
                    chcp 65001
                    :start
                    echo 开始启动MC服务器
                    {command}
                    echo MC服务器已关闭
                    echo 服务器正在重新启动..。
                    echo 按 CTRL + C 停止。
                    goto :start
                """))
            else:
                fp.write(_(f"""
                    @echo off
                    chcp 65001
                    echo 开始启动MC服务器
                    {command}
                    echo MC服务器已关闭
                    pause
                """))
    elif os_name == "Linux":
        with open("start.sh", "w", encoding="utf8") as fp:
            if restart:
                fp.write(_(f"""
                    #!/bin/bash
                    echo "开始启动MC服务器"
                    {command}
                    echo "MC服务器已关闭"
                    while true; do
                        echo "按 CTRL + C 停止。"
                        {command}
                        sleep 1
                    done
                """))
            else:
                fp.write(_(f"""
                    #!/bin/bash
                    echo "开始启动MC服务器"
                    {command}
                    echo "MC服务器已关闭"
                """))
    else:
        raise OSError("不支持的操作系统")


if __name__ == "__main__":
    server = detect_jar()
    if server is None:
        exit_()
    command = generate_command(server, detect_brand(server))
    generate_batch(command, ask("开启自动重启?"))
    print("生成完毕")
    exit_()
