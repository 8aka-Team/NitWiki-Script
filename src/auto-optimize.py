import os.path
from utils import *
import rtoml as toml

script_license()

print("开始优化!")

danger = ask("是否开启危险优化(会严重影响玩家体验)?")


@handler('server.properties', ServerPropLoader.load, ServerPropLoader.dump)
def optimize_prop(properties):
    properties["view-distance"] = 7
    properties["allow-flight"] = "true"
    properties["use-native-transport"] = "true"
    properties["simulation-distance"] = 4


@handler('bukkit.yml')
def optimize_bukkit(bukkit):
    bukkit["spawn-limits"] = {
        "monsters": 20,
        "animals": 5,
        "water-animals": 2,
        "water-ambient": 2,
        "ambient": 1,
        "axolotls": 3,
        "water-underground-creature": 3
    }
    bukkit["chunk-gc"]["period-in-ticks"] = 400
    bukkit["ticks-per"] = {
        "animal-spawns": 400,
        "monster-spawns": 10,
        "water-spawns": 400,
        "water-ambient-spawns": 400,
        "water-underground-creature-spawns": 400,
        "axolotl-spawns": 400,
        "ambient-spawns": 400,
        "autosave": 6000
    }


@handler('spigot.yml')
def optimize_spigot(spigot):
    spigot["world-settings"]["default"]["mob-spawn-range"] = 3
    r = spigot["world-settings"]["default"]["entity-activation-range"]
    r["animals"] = 16
    r["monsters"] = 24
    r["raiders"] = 48
    r["misc"] = 8
    r["water"] = 8
    r["villagers"] = 16
    r["flying-monsters"] = 48
    r["tick-inactive-villagers"] = False
    spigot["world-settings"]["default"]["nerf-spawner-mobs"] = True
    spigot["world-settings"]["default"]["merge-radius"] = {
        "item": 3.5,
        "exp": 4.0
    }
    if danger:
        spigot["world-settings"]["default"]["ticks-per"] = {
            "hopper-transfer": 4,
            "hopper-check": 4
        }


@handler(r'config/paper-global.yml')
def optimize_paper_global(paper):
    paper["timings"]["enabled"] = False


@handler("paper.yml" if os.path.isfile("paper.yml") else r'config/paper-world-defaults.yml')
def optimize_paper_world(paper):
    paper["chunks"]["delay-chunk-unloads-by"] = "10s"
    paper["chunks"]["max-auto-save-chunks-per-tick"] = 8
    paper["chunks"]["prevent-moving-into-unloaded-chunks"] = True
    paper["chunks"]["entity-per-chunk-save-limit"] = {
        "area_effect_cloud": 8,
        "arrow": 16,
        "breeze_wind_charge": 8,
        "dragon_fireball": 3,
        "egg": 8,
        "ender_pearl": 8,
        "experience_bottle": 3,
        "experience_orb": 16,
        "eye_of_ender": 8,
        "fireball": 8,
        "firework_rocket": 8,
        "llama_spit": 3,
        "potion": 8,
        "shulker_bullet": 8,
        "small_fireball": 8,
        "snowball": 8,
        "spectral_arrow": 16,
        "trident": 16,
        "wither_skull": 4
    }
    paper["entities"]["armor-stands"]["tick"] = False
    paper["entities"]["armor-stands"]["do-collision-entity-lookups"] = False
    paper["entities"]["spawning"]["alt-item-despawn-rate"] = {
        "enabled": True,
        "items": {
            "cobblestone": 300,
            "netherrack": 300,
            "sand": 300,
            "red_sand": 300,
            "gravel": 300,
            "dirt": 300,
            "short_grass": 300,
            "pumpkin": 300,
            "melon_slice": 300,
            "kelp": 300,
            "bamboo": 300,
            "sugar_cane": 300,
            "twisting_vines": 300,
            "weeping_vines": 300,
            "oak_leaves": 300,
            "spruce_leaves": 300,
            "birch_leaves": 300,
            "jungle_leaves": 300,
            "acacia_leaves": 300,
            "dark_oak_leaves": 300,
            "cherry_leaves": 300,
            "mangrove_leaves": 300,
            "cactus": 300,
            "diorite": 300,
            "granite": 300,
            "andesite": 300,
            "scaffolding": 600
        }
    }

    paper["entities"]["spawning"]["despawn-ranges"] = {
        "ambient": {
            "hard": 72,
            "soft": 30
        },
        "axolotls": {
            "hard": 72,
            "soft": 30
        },
        "creature": {
            "hard": 72,
            "soft": 30
        },
        "misc": {
            "hard": 72,
            "soft": 30
        },
        "monster": {
            "hard": 72,
            "soft": 30
        },
        "underground_water_creature": {
            "hard": 72,
            "soft": 30
        },
        "water_ambient": {
            "hard": 72,
            "soft": 30
        },
        "water_creature": {
            "hard": 72,
            "soft": 30
        }
    }
    paper["entities"]["spawning"]["non-player-arrow-despawn-rate"] = 20
    paper["entities"]["spawning"]["creative-arrow-despawn-rate"] = 20
    if not danger:
        paper["entities"]["behavior"]["spawner-nerfed-mobs-should-jump"] = True
    paper["collisions"]["max-entity-collisions"] = 2
    paper["collisions"]["fix-climbing-bypassing-cramming-rule"] = True
    paper["misc"]["update-pathfinding-on-block-update"] = False
    paper["misc"]["redstone-implementation"] = "ALTERNATE_CURRENT"
    if not (os.path.exists("pufferfish.yml") or
            os.path.exists("leaf_config/leaf_global_config.toml") or
            os.path.exists("config/leaf-global.yml")):
        paper["tick-rates"]["behavior"] = {
            "villager": {
                "validatenearbypoi": 60,
                "acquirepoi": 120
            }
        }
        paper["tick-rates"]["sensor"] = {
            "villager": {
                "secondarypoisensor": 80,
                "nearestbedsensor": 80,
                "villagerbabiessensor": 40,
                "playersensor": 40,
                "nearestlivingentitysensor": 40
            }
        }
    paper["hopper"]["disable-move-event"] = False
    paper["hopper"]["ignore-occluding-blocks"] = True
    paper["tick-rates"]["mob-spawner"] = 2
    paper["tick-rates"]["grass-spread"] = 4
    paper["tick-rates"]["container-update"] = 1
    paper["environment"]["optimize-explosions"] = True
    if danger:
        paper["environment"]["treasure-maps"]["enabled"] = False
        paper["environment"]["nether-ceiling-void-damage-height"] = 127
    paper["environment"]["treasure-maps"]["find-already-discovered"] = {
        "loot-tables": True,
        "villager-trade": True
    }
    paper["tick-rates"]["wet-farmland"] = 2
    paper["spawn"]["keep-spawn-loaded"] = False
    paper["spawn"]["keep-spawn-loaded-range"] = 3


@handler('config/gale-world-defaults.yml')
def optimize_gale_world(gale):
    gale["small-optimizations"]["max-projectile-chunk-loads"]["per-tick"] = 2
    gale["small-optimizations"]["max-projectile-chunk-loads"]["per-projectile"][
        "reset-movement-after-reach-limit"] = True
    if danger:
        gale["small-optimizations"]["max-projectile-chunk-loads"]["per-projectile"][
            "remove-from-world-after-reach-limit"] = True
    gale["small-optimizations"]["reduced-intervals"]["acquire-poi-for-stuck-entity"] = 200
    gale["small-optimizations"]["reduced-intervals"]["check-nearby-item"]["hopper"]["interval"] = 50
    gale["small-optimizations"]["reduced-intervals"]["check-nearby-item"]["hopper"]["minecart"]["temporary-immunity"][
        "duration"] = 75
    gale["small-optimizations"]["reduced-intervals"]["check-nearby-item"]["hopper"]["minecart"]["temporary-immunity"][
        "nearby-item-max-age"] = 600
    gale["gameplay-mechanics"]["arrow-movement-resets-despawn-counter"] = False
    gale["small-optimizations"]["save-fireworks"] = False


@handler('config/gale-global.yml')
def optimize_gale_global(gale):
    gale["small-optimizations"]["reduced-intervals"]["increase-time-statistics"] = 100
    gale["small-optimizations"]["reduced-intervals"]["update-entity-line-of-sight"] = 10


@handler('pufferfish.yml')
def optimize_pufferfish(pufferfish):
    pufferfish["projectile"]["max-loads-per-projectile"] = 8
    dab = pufferfish["dab"]
    dab["enabled"] = True
    dab["max-tick-freq"] = 20
    dab["activation-dist-mod"] = 7
    pufferfish["enable-async-mob-spawning"] = True
    pufferfish["enable-suffocation-optimization"] = True
    pufferfish["inactive-goal-selector-throttle"] = True
    pufferfish["misc"]["disable-method-profiler"] = True


@handler('purpur.yml')
def optimize_purpur(purpur):
    purpur["settings"]["use-alternate-keepalive"] = True
    purpur["world-settings"]["default"]["mobs"]["zombie"]["aggressive-towards-villager-when-lagging"] = False
    if not danger:
        purpur["settings"]["lagging-threshold"] = 18
    if danger:
        purpur["world-settings"]["default"]["mobs"]["villager"]["lobotomize"]["enabled"] = True
        purpur["world-settings"]["default"]["mobs"]["villager"]["lobotomize"]["search-radius"] = {
            "acquire-poi": 16,
            "nearest-bed-sensor": 16
        }
        purpur["world-settings"]["default"]["mobs"]["dolphin"]["disable-treasure-searching"] = True
    purpur["world-settings"]["default"]["gameplay-mechanics"]["entities-can-use-portals"] = False
    purpur["world-settings"]["default"]["gameplay-mechanics"]["player"]["teleport-if-outside-border"] = True


@handler("leaf_config/leaf_global_config.toml", toml.load, toml.dump)
def optimize_leaf_legacy(leaf):
    leaf["async"]["async_pathfinding"]["enabled"] = True
    leaf["async"]["async_mob_spawning"]["enabled"] = True
    if ask("使用的是Java 21+"):
        leaf["performance"]["use_virtual_thread_for_async_scheduler"]["enabled"] = True
    leaf["performance"]["optimize_minecart"]["enabled"] = True
    dab = leaf["performance"]["dab"]
    dab["max-tick-freq"] = 20
    dab["activation-dist-mod"] = 7
    leaf["gameplay"]["disable_moved_wrongly_threshold"]["enabled"] = True
    leaf["performance"]["use_faster_random_generator"]["enabled"] = True


@handler("config/leaf-global.yml")
def optimize_leaf_global(leaf):
    leaf["async"]["async-pathfinding"]["enabled"] = True
    leaf["async"]["async-mob-spawning"]["enabled"] = True
    leaf["async"]["async-entity-tracker"]["enabled"] = True
    leaf["async"]["async-locator"]["enabled"] = True
    leaf["async"]["async-playerdata-save"]["enabled"] = True
    leaf["async"]["async-chunk-send"]["enabled"] = True
    if ask("使用 Citizens"):
        leaf["async"]["async-entity-tracker"]["compat-mode"] = True
    if danger:
        leaf["performance"]["throttle-hopper-when-full"]["enabled"] = True
    leaf["performance"]["use-virtual-thread-for-async-scheduler"] = True
    leaf["performance"]["reduce-packets"]["reduce-entity-move-packets"] = True
    leaf["performance"]["optimize-minecart"]["enabled"] = True
    leaf["performance"]["faster-random-generator"]["enabled"] = True
    leaf["performance"]["faster-random-generator"]["enable-for-worldgen"] = True
    leaf["performance"]["create-snapshot-on-retrieving-blockstate"] = False
    if not danger:
        leaf["performance"]["faster-random-generator"]["use-legacy-random-for-slime-chunk"] = True
    dab = leaf["performance"]["dab"]
    dab["max-tick-freq"] = 20
    dab["activation-dist-mod"] = 7
    dab["start-distance"] = 8
    if not danger:
        dab["dont-enable-if-in-water"] = True
    leaf["performance"]["dont-save-entity"]["dont-save-primed-tnt"] = True
    leaf["performance"]["dont-save-entity"]["dont-save-falling-block"] = True
    leaf["performance"]["entity-timeouts"]["SNOWBALL"] = 200
    leaf["performance"]["entity-timeouts"]["LLAMA_SPIT"] = 150
    leaf["performance"]["entity-timeouts"]["DRAGON_FIREBALL"] = 150
    leaf["performance"]["entity-timeouts"]["EGG"] = 300
    leaf["performance"]["entity-timeouts"]["FIREBALL"] = 600
    leaf["performance"]["entity-timeouts"]["SMALL_FIREBALL"] = 400
    leaf["performance"]["entity-timeouts"]["WIND_CHARGE"] = 200
    leaf["performance"]["entity-timeouts"]["BREEZE_WIND_CHARGE"] = 200
    leaf["performance"]["entity-timeouts"]["WITHER_SKULL"] = 200
    leaf["gameplay-mechanisms"]["player"]["disable-moved-wrongly-threshold"] = True
    leaf["misc"]["lag-compensation"]["enabled"] = True
    leaf["misc"]["lag-compensation"]["enable-for-water"] = True
    leaf["misc"]["lag-compensation"]["enable-for-lava"] = True
    leaf["network"]["connection-flush-queue-rewrite"] = True


if __name__ == "__main__":
    optimize_prop()
    optimize_bukkit()
    optimize_spigot()
    optimize_paper_global()
    optimize_paper_world()
    optimize_pufferfish()
    optimize_purpur()
    optimize_gale_world()
    optimize_gale_global()
    if not os.path.exists("purpur.yml"):
        print("Purpur尚未安装")
        print("为什么不试一下Purpur呢？")
    optimize_leaf_legacy()
    optimize_leaf_global()
    exit_()
