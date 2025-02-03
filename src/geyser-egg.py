from utils import *

script_license()


def main():
    if not os.path.exists("plugins/Geyser-Spigot"):
        print("Geyser和Floodgate尚未安装")
        install_geyser()
        print("安装完成,启动服务器,在关闭后执行此脚本")
        exit_()
    print("已安装Geyser和Floodgate")
    auto_install = ask("简单模式(跳过询问)")
    setup_geyser(auto_install)
    setup_floodgate(auto_install)
    install_extend(auto_install)
    setup_plugin(auto_install)
    print("已完成")
    exit_()


def install_geyser():
    download("https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/spigot",
             "plugins/Geyser-Spigot.jar")

    download("https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest/downloads/spigot",
             "plugins/floodgate.jar")


@handler("plugins/Geyser-Spigot/config.yml")
def setup_geyser(geyser, auto_install=False):
    prop = ServerPropLoader.load(open("server.properties", "r"))
    server_port = int(prop["port"])
    geyser["remote"]["port"] = server_port
    if auto_install or ask("允许Geyser玩家在地狱上层(y>128)放置方块"):
        geyser["above-bedrock-nether-building"] = True


@handler("plugins/floodgate/config.yml")
def setup_floodgate(floodgate, auto_install=False):
    floodgate["username-prefix"] = "BE_" if auto_install else input(
        "\033[33m基岩版玩家用户名前缀(默认为.,推荐BE_):\033[0m")


def install_extend(auto_install=False):
    if auto_install or ask("安装GeyserOptionalPack(推荐)"):
        download("https://download.geysermc.org/v2/projects/geyseroptionalpack/versions/latest/builds/latest"
                 "/downloads/geyseroptionalpack", "plugins/Geyser-Spigot/packs/geyseroptionalpack.mcpack")
    if auto_install or ask("安装Geyser行为修复(推荐)"):
        download("https://github.com/GeyserMC/Hurricane/releases/download/2.0-SNAPSHOT-1/Hurricane.jar",
                 "plugins/Hurricane.jar")
        download("https://github.com/tbyt/BedrockParity/releases/download/release/BedrockParity.jar",
                 "plugins/BedrockParity.jar")
    if auto_install or ask("安装皮肤修复(推荐)"):
        download("https://github.com/Camotoy/GeyserSkinManager/releases/download/1.7/GeyserSkinManager-Spigot.jar",
                 "plugins/GeyserSkinManager-Spigot.jar")
    if auto_install or ask("安装GeyserUtils(推荐)"):
        download("https://github.com/zimzaza4/GeyserUtils/releases/download/1.0.0-fix/geyserutils-spigot-1.0-SNAPSHOT"
                 ".jar", "plugins/geyserutils-spigot-1.0-SNAPSHOT.jar")
        download("https://github.com/zimzaza4/GeyserUtils/releases/download/1.0.0-fix/geyserutils-geyser-1.0-SNAPSHOT"
                 ".jar", "plugins/Geyser-Spigot/extensions/geyserutils-geyser-1.0-SNAPSHOT.jar")
    if auto_install or ask("安装更好的第三人称视角(推荐)(需要GeyserUtils)"):
        download("https://github.com/lilingfengdev/GeyserBetterBedrockThirdPerson/releases/download/latest"
                 "/BetterBedrockThirdPerson-1.0-SNAPSHOT.jar", "plugins/BetterBedrockThirdPerson-1.0-SNAPSHOT.jar")
    if not auto_install and ask("安装第三方披风/耳朵支持"):
        download(
            "https://download.geysermc.org/v2/projects/thirdpartycosmetics/versions/latest/builds/latest/downloads"
            "/thirdpartycosmetics",
            "plugins/Geyser-Spigot/extensions/ThirdPartyCosmetics.jar")
    if auto_install or ask("安装Geyser自动更新"):
        download("https://ci.kejonamc.dev/job/GeyserUpdater/job/main/18/artifact/target/GeyserUpdater-1.6.4.jar",
                 "plugins/GeyserUpdater-1.6.4.jar")
    if not auto_install and ask("安装Geyser扩展(1.20.6+)"):
        download("https://cdn.modrinth.com/data/OguISbmK/versions/QDtr4UOA/GeyserExtras_CN.jar",
                 "plugins/GeyserExtras.jar")


def setup_plugin(auto_install=False):
    if os.path.exists("plugins/Slimefun") and ask("安装Slimefun材质兼容(需要Slimefun Resource Pack)"):
        download("https://qcymc.cloud/f/QWRHo/Slimefun.mcpack", "plugins/Geyser-Spigot/packs/Slimefun.mcpack")
        download("https://qcymc.cloud/f/R6DT5/RYSurvival-SlimefunMapping.jar",
                 "plugins/Geyser-Spigot/extensions/RYSurvival-SlimefunMapping.jar")
    if os.path.exists("plugins/Residence") and (auto_install or ask("安装Residence基岩版菜单兼容")):
        download("https://github.com/RenYuan-MC/ResidenceForm/releases/download/dev/ResidenceForm.jar",
                 "plugins/ResidenceForm.jar")
    if (os.path.exists("plugins/QuickShop-Hikari") or os.path.exists("plugins/QuickShop")) and (
            auto_install or ask("安装QuickShop基岩版菜单兼容")):
        download("https://github.com/RenYuan-MC/QuickShopForm/releases/download/dev/QuickShopForm.jar",
                 "plugins/QuickShopForm.jar")
    if auto_install or ask("安装Geyser扩展菜单(BedrockPlayerSupport)"):
        download("https://github.com/DongShaoNB/BedrockPlayerSupport/releases/download/v2.0.0/BedrockPlayerSupport-2"
                 ".0.0-all.jar", "plugins/BedrockPlayerSupport.jar")
    if os.path.exists("plugins/Skript") and (auto_install or ask("安装Skript基岩版兼容")):
        download("https://github.com/kejonaMC/floodgate-skript/releases/download/v2.1/floodgate-skript-2.1.jar",
                 "plugins/floodgate-skript-2.1.jar")

    if ask("安装基岩版菜单制作插件"):
        download("https://dl.8aka.org/plugins/MagicMenu-1.0.3.jar",
                 "plugins/Geyser-Spigot/extensions/MagicMenu-1.0.3.jar")


if __name__ == "__main__":
    main()
