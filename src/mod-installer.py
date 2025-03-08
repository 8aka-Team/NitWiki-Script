import subprocess
import xml.etree.ElementTree as ET
from utils import *

script_license()

def get_latest_fabric_loader():
    url = "https://bmclapi2.bangbang93.com/fabric-meta/v2/versions/loader"
    response = requests.get(url)
    loaders = response.json()
    for loader in loaders:
        if loader['stable']:
            return loader['version']
    return None


def get_latest_fabric_installer():
    url = "https://bmclapi2.bangbang93.com/fabric-meta/v2/versions/installer"
    response = requests.get(url)
    installers = response.json()
    return installers[0]['version']


def get_fabric_api_version(mc_version):
    try:
        url = "https://bmclapi2.bangbang93.com/maven/net/fabricmc/fabric-api/fabric-api/maven-metadata.xml"
        response = requests.get(url)
        root = ET.fromstring(response.text)
        versions = [v.text for v in root.findall('.//version')]
        for version in reversed(versions):
            if f"+{mc_version}" in version:
                return version
        return None
    except Exception as e:
        print(f"获取Fabric API版本失败: {e}")
        return None


def install_fabric(mc_version, install_dir):
    print("\n=== 开始安装Fabric ===")

    # 获取组件版本
    loader_version = get_latest_fabric_loader()
    installer_version = get_latest_fabric_installer()

    if not loader_version or not installer_version:
        print("无法获取Fabric组件版本")
        return

    print(f"1. 检测到最新Fabric Loader: {loader_version}")

    # 下载安装器
    installer_url = f"https://maven.fabricmc.net/net/fabricmc/fabric-installer/{installer_version}/fabric-installer-{installer_version}.jar"
    installer_path = os.path.join(install_dir, "fabric-installer.jar")
    print("2. 下载Fabric安装器...")
    download(installer_url, installer_path)

    # 运行安装器
    print("3. 运行安装器...")
    subprocess.run([
        "java", "-jar", installer_path,
        "server", "-mcversion", mc_version,
        "-loader", loader_version,
        "-downloadMinecraft",
        "-dir", install_dir
    ], check=True, encoding='utf-8')

    # 下载Fabric API
    print("4. 下载Fabric API...")
    api_version = get_fabric_api_version(mc_version)
    if api_version:
        api_url = f"https://maven.fabricmc.net/net/fabricmc/fabric-api/fabric-api/{api_version}/fabric-api-{api_version}.jar"
        mods_dir = os.path.join(install_dir, "mods")
        os.makedirs(mods_dir, exist_ok=True)
        download(api_url, os.path.join(mods_dir, os.path.basename(api_url)))
    else:
        print("警告: 无法自动获取Fabric API版本，请手动下载")

    print("=== Fabric安装完成 ===")


def get_forge_versions(mc_version):
    url = f"https://bmclapi2.bangbang93.com/forge/minecraft/{mc_version}"
    response = requests.get(url)
    return response.json()


def install_forge(mc_version, install_dir):
    print("\n=== 开始安装Forge ===")

    # 获取版本列表
    versions = get_forge_versions(mc_version)
    if not versions:
        print("未找到可用的Forge版本")
        return

    # 选择最新版本
    latest = max(versions, key=lambda x: x['build'])
    forge_version = latest['version']
    print(f"1. 检测到最新Forge版本: {forge_version}")

    # 下载安装器
    print("2. 下载Forge安装器...")
    download_url = f"https://bmclapi2.bangbang93.com/forge/download?mcversion={mc_version}&version={forge_version}&category=installer&format=jar"
    response = requests.get(download_url, allow_redirects=False)
    if response.status_code != 302:
        print("获取下载地址失败")
        return

    installer_path = os.path.join(install_dir, "forge-installer.jar")
    download(response.url, installer_path)

    # 运行安装器
    print("3. 运行安装器...")
    subprocess.run([
        "java", "-jar", installer_path,
        "--installServer",
        install_dir
    ], check=True, cwd=install_dir)

    print("=== Forge安装完成 ===")


def get_neoforge_versions(mc_version):
    url = f"https://bmclapi2.bangbang93.com/neoforge/list/{mc_version}"
    response = requests.get(url)
    return response.json()


def install_neoforge(mc_version, install_dir):
    print("\n=== 开始安装NeoForge ===")

    # 获取版本列表
    versions = get_neoforge_versions(mc_version)
    if not versions:
        print("未找到可用的NeoForge版本")
        return

    # 选择最新版本
    latest = versions[-1]
    version = latest['version']
    print(f"1. 检测到最新NeoForge版本: {version}")

    # 下载安装器
    print("2. 下载NeoForge安装器...")
    download_url = f"https://bmclapi2.bangbang93.com/neoforge/version/{version}/download/installer"
    response = requests.get(download_url, allow_redirects=False)
    if response.status_code != 302:
        print("获取下载地址失败")
        return

    installer_path = os.path.join(install_dir, "neoforge-installer.jar")
    download(response.url, installer_path)

    # 运行安装器
    print("3. 运行安装器...")
    subprocess.run([
        "java", "-jar", installer_path,
        "--installServer",
        install_dir
    ], check=True, cwd=install_dir)

    print("=== NeoForge安装完成 ===")


def main():
    print("Minecraft 服务端安装程序")
    print("支持平台: Forge | NeoForge | Fabric\n")

    # 用户输入
    loader = input("请选择要安装的 Mod 加载器 (1: Forge, 2: NeoForge, 3: Fabric): ")
    mc_version = input("请输入 Minecraft 版本号 (例如 1.20.1): ")
    install_dir = input("请输入安装目录 (默认当前目录): ") or "."

    install_dir = os.path.abspath(install_dir)
    os.makedirs(install_dir, exist_ok=True)

    if loader == '1':
        install_forge(mc_version, install_dir)
    elif loader == '2':
        install_neoforge(mc_version, install_dir)
    elif loader == '3':
        install_fabric(mc_version, install_dir)
    else:
        print("无效的选择")


if __name__ == "__main__":
    main()