import json
from mojang import API
import os

api = API()
player_dir = '/home/karl/CelestialVanilla/world/stats/'


class PlayerStats:

    def __init__(self, player, param1, param2):
        self.player = player
        self.param1 = param1
        self.param2 = param2

    async def get_stats(self):
        uuid = api.get_uuid(self.player)
        # Get stats of player from dict. also handle 404 response.
        return uuid

    async def find_stats(self):
        uuid = await self.get_stats()
        files = os.scandir(player_dir)
        for file in files:
            if file.name[:8] in uuid:
                with open(player_dir + file.name) as f:
                    content = json.load(f)
                    return content['stats'][self.param1][self.param2]

    async def write_totals(self):
        logistics = 0
        building = 0
        mining = 0
        logging = 0
        crafting = 0
        fishing = 0
        farming = 0
        logging_arr = ['minecraft:oak_wood', 'minecraft:birch_wood', 'minecraft:spruce_wood', 'minecraft:acacia_wood',
                       'minecraft:jungle_wood', 'minecraft:mangrove_wood', 'minecraft:dark_oak_wood',
                       'minecraft:cherry_wood']
        farming_arr = ['minecraft:wheat', 'minecraft:kelp', 'minecraft:sugar_cane', 'minecraft:potatoes',
                       'minecraft:bamboo', 'minecraft:beetroots', 'minecraft:carrots', 'minecraft:sweet_berry_bush']
        logistics_arr = ['minecraft:swim_one_cm', 'minecraft:fly_one_cm', 'minecraft:sprint_one_cm',
                         'minecraft:walk_one_cm', 'minecraft:boat_one_cm']
        files = os.scandir(player_dir)
        for file in files:
            with open(file) as f:
                content = json.load(f)
                if not content['stats'].get('minecraft:used') is None:
                    building_keys = content['stats']['minecraft:used'].keys()
                if not content['stats'].get('minecraft:crafted') is None:
                    crafting_keys = content['stats']['minecraft:crafted'].keys()
                if not content['stats'].get('minecraft:mined') is None:
                    mining_keys = content['stats']['minecraft:mined'].keys()
                if not content['stats'].get('minecraft:mined') is None:
                    for index in logging_arr:
                        if not content['stats']['minecraft:mined'].get(index) is None:
                            logging = logging + content['stats']['minecraft:mined'][index]
                if not content['stats'].get('minecraft:mined') is None:
                    for index in farming_arr:
                        if not content['stats']['minecraft:mined'].get(index) is None:
                            farming = farming + content['stats']['minecraft:mined'][index]
                if not content['stats'].get('minecraft:custom') is None:
                    for index in logistics_arr:
                        if not content['stats']['minecraft:custom'].get(index) is None:
                            logistics = logistics + content['stats']['minecraft:custom'][index]
                if not content['stats'].get('minecraft:custom') is None:
                    if not content['stats']['minecraft:custom'].get('minecraft:fish_caught') is None:
                        fishing = fishing + content['stats']['minecraft:custom']['minecraft:fish_caught']
                if not content['stats'].get('minecraft:used') is None:
                    for key in building_keys:
                        building = building + content['stats']['minecraft:used'][key]
                if not content['stats'].get('minecraft:crafted') is None:
                    for key in crafting_keys:
                        crafting = crafting + content['stats']['minecraft:crafted'][key]
                if not content['stats'].get('minecraft:used') is None:
                    for key in mining_keys:
                        mining = mining + content['stats']['minecraft:mined'][key]
        building = building - mining
        result_dict = {'logging': logging, 'mining': mining, 'fishing': fishing, 'crafting': crafting,
                       'building': building, 'farming': farming, 'logistics': logging}
        with open('totals.json', 'w') as f:
            json.dump(result_dict, f)
