import os.path

from utils import *

script_license()

hide_air_block = ask("隐藏空气中的矿石(可能会导致性能问题)")
hide_lava_block = ask("隐藏岩浆中的矿石")


def hide_ext(config):
    if hide_air_block:
        config["anticheat"]["anti-xray"]["hidden-blocks"].append("air")
    if hide_lava_block:
        config["anticheat"]["anti-xray"]["lava-obscures"] = True


def antixray_config(config):
    config["anticheat"] = {"anti-xray": {}}


@handler(r'config/paper-world-defaults.yml')
def config_paper_world(paper):
    antixray_config(paper)
    paper["anticheat"]["anti-xray"] = {
        "enabled": True,
        "engine-mode": 1,
        "hidden-blocks": [
            "chest",
            "coal_ore",
            "deepslate_coal_ore",
            "copper_ore",
            "deepslate_copper_ore",
            "raw_copper_block",
            "diamond_ore",
            "deepslate_diamond_ore",
            "emerald_ore",
            "deepslate_emerald_ore",
            "gold_ore",
            "deepslate_gold_ore",
            "iron_ore",
            "deepslate_iron_ore",
            "raw_iron_block",
            "lapis_ore",
            "deepslate_lapis_ore",
            "redstone_ore",
            "deepslate_redstone_ore"
        ],
        "lava-obscures": False,
        "max-block-height": 64,
        "replacement-blocks": [],
        "update-radius": 2,
        "use-permission": False
    }
    hide_ext(paper)


@handler(r'world_nether/paper-world.yml')
def config_paper_nether(paper):
    antixray_config(paper)
    paper["anticheat"]["anti-xray"] = {
        "enabled": True,
        "engine-mode": 1,
        "hidden-blocks": [
            "ancient_debris",
            "nether_gold_ore",
            "nether_quartz_ore"
        ],
        "lava-obscures": False,
        "max-block-height": 128,
        "replacement-blocks": [],
        "update-radius": 2,
        "use-permission": False
    }
    hide_ext(paper)


@handler(r'world_the_end/paper-world.yml')
def config_paper_end(paper):
    antixray_config(paper)
    paper["anticheat"]["anti-xray"]["enabled"] = False

def config_raytrace():
    with open("plugins/RayTraceAntiXray/config.yml","w",encoding="utf-8") as handler:
        if ask("使用 RayTraceAntiXray 优化配置(选NO使用安全配置)"):
            handler.write("""
settings:
  anti-xray:
    update-ticks: 1
    ms-per-ray-trace-tick: 50
    # 根据可用的（最好是未使用的）CPU线程进行调整。
    ray-trace-threads: 2
world-settings:
  default:
    anti-xray:
      ray-trace: true
      ray-trace-third-person: false
      ray-trace-distance: 64.0
      rehide-blocks: false
      rehide-distance: .inf
      max-ray-trace-block-count-per-chunk: 30
      ray-trace-blocks:
      # 你可以在这里添加更多的方块，
      # 但可能需要调整max-ray-trace-block-count-per-chunk设置。
      - chest
      - diamond_ore
      - deepslate_diamond_ore
      - emerald_ore
      - deepslate_emerald_ore
      - gold_ore
      - deepslate_gold_ore
      - lapis_ore
      - deepslate_lapis_ore
      - spawner
  world_nether:
    anti-xray:
      # 注意，ancient_debris(下界合金)永远不会自然生成在暴露于空气的地方。
      # 普通引擎模式：1已经足够，在下界禁用射线追踪。
      ray-trace: false
  # 调整世界名称。
  world_the_end:
    anti-xray:
      ray-trace: false
            """)
        else:
            handler.write("""
settings:
  anti-xray:
    update-ticks: 1
    ms-per-ray-trace-tick: 50
    # 根据可用的（最好是未使用的）CPU线程进行调整。
    ray-trace-threads: 2
world-settings:
  default:
    anti-xray:
      ray-trace: true
      # 请注意，这大约需要三倍的资源。
      ray-trace-third-person: true
      ray-trace-distance: 80.0
      rehide-blocks: true
      rehide-distance: 76.0
      max-ray-trace-block-count-per-chunk: 60
      ray-trace-blocks:
      # 您可以在此处添加更多方块，
      # 但可能需要调整max-ray-trace-block-count-per-chunk设置。
      - chest
      - diamond_ore
      - deepslate_diamond_ore
      - emerald_ore
      - deepslate_emerald_ore
      - gold_ore
      - deepslate_gold_ore
      - lapis_ore
      - deepslate_lapis_ore
      - mossy_cobblestone
      - spawner
  # 调整世界名称。
  world_nether:
    anti-xray:
      # 注意，ancient_debris(下界合金)永远不会自然生成在暴露于空气的地方。
      # 普通引擎模式：1已经足够，在下界禁用射线追踪。
      ray-trace: false
  # 调整世界名称。
  world_the_end:
    anti-xray:
      ray-trace: false
            """)
if __name__ == "__main__":
    config_paper_world()
    config_paper_nether()
    config_paper_end()
    if os.path.exists("plugins/RayTraceAntiXray/config.yml"):
        config_raytrace()
    exit_()
