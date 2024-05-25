from utils import *

script_license()


def main():
    if not os.path.exists("plugins/Geyser-Spigot"):
        print("Geyser和Floodgate尚未安装")
        install_geyser()
        print("安装完成,启动服务器,在关闭后执行此脚本")
        exit_()
    print("已安装Geyser和Floodgate")
    setup_geyser()
    setup_floodgate()
    install_extend()
    exit_()


def install_geyser():
    download("https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/spigot",
             "plugins/Geyser-Spigot.jar")

    download("https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest/downloads/spigot",
             "plugins/floodgate.jar")


@handler("plugins/Geyser-Spigot/config.yml")
def setup_geyser(geyser):
    prop = ServerPropLoader()
    server_port = int(prop.data["port"])
    geyser["remote"]["port"] = server_port
    if ask("允许Geyser玩家在地狱上层(y>128)放置方块"):
        geyser["above-bedrock-nether-building"] = True

    if ask("开启XBox成绩获得"):
        geyser["xbox-achievements-enabled"] = True


@handler("plugins/floodgate/config.yml")
def setup_floodgate(floodgate):
    prefix = input("\033[33m基岩版玩家用户名前缀(默认为.,推荐BE_):\033[0m")
    floodgate["username-prefix"] = prefix


def install_extend():
    if ask("安装GeyserOptionalPack(推荐)"):
        download("https://download.geysermc.org/v2/projects/geyseroptionalpack/versions/latest/builds/latest"
                 "/downloads/geyseroptionalpack", "plugins/Geyser-Spigot/packs/geyseroptionalpack.mcpack")
    if ask("安装Geyser行为修复(推荐)"):
        download("https://github.com/GeyserMC/Hurricane/releases/download/2.0-SNAPSHOT-1/Hurricane.jar",
                 "plugins/Hurricane.jar")
        download("https://github.com/tbyt/BedrockParity/releases/download/release/BedrockParity.jar",
                 "plugins/BedrockParity.jar")
    if ask("安装皮肤修复(推荐)"):
        download("https://github.com/Camotoy/GeyserSkinManager/releases/download/1.7/GeyserSkinManager-Spigot.jar",
                 "plugins/GeyserSkinManager-Spigot.jar")
    if ask("安装箱子菜单修复"):
        download("https://gitee.com/xi-bohan/BedrockChestUI/releases/download/BedrockChestUI/ChstomChest0.2.mcpack",
                 "plugins/Geyser-Spigot/packs/ChstomChest0.2.mcpack")
        download("https://gitee.com/xi-bohan/BedrockChestUI/releases/download/BedrockChestUI/BedrockChestUI-1.0.5.jar",
                 "plugins/BedrockChestUI-1.0.5.jar")
    if ask("安装GeyserUtils(推荐)"):
        download("https://github.com/zimzaza4/GeyserUtils/releases/download/1.0.0-fix/geyserutils-spigot-1.0-SNAPSHOT"
                 ".jar", "plugins/geyserutils-spigot-1.0-SNAPSHOT.jar")
        download("https://github.com/zimzaza4/GeyserUtils/releases/download/1.0.0-fix/geyserutils-geyser-1.0-SNAPSHOT"
                 ".jar", "plugins/Geyser-Spigot/extensions/geyserutils-geyser-1.0-SNAPSHOT.jar")
    if ask("安装更好的第三人称视角(推荐)(需要GeyserUtils)"):
        download("https://github.com/lilingfengdev/GeyserBetterBedrockThirdPerson/releases/download/latest"
                 "/BetterBedrockThirdPerson-1.0-SNAPSHOT.jar", "plugins/BetterBedrockThirdPerson-1.0-SNAPSHOT.jar")
    if ask("安装Luckperms基岩版支持"):
        download("https://qcymc.cloud/f/mZLhW/[MineBBS]-LuckBedrock-1.1.jar", "plugins/LuckBedrock-1.1.jar")


if __name__ == "__main__":
    main()