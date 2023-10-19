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
        logging_arr = ['minecraft:oak_wood', 'minecraft:birch_wood', 'minecraft:spruce_wood', 'minecraft:acacia_wood',
                       'minecraft:jungle_wood', 'minecraft:mangrove_wood', 'minecraft:dark_oak_wood',
                       'minecraft:cherry_wood']
        farming_arr = ['minecraft:wheat', 'minecraft:kelp', 'minecraft:sugar_cane', 'minecraft:potatoes',
                       'minecraft:bamboo', 'minecraft:beetroots', 'minecraft:carrots', 'minecraft:sweet_berry_bush']
        logistics_arr = ['minecraft:swim_one_cm', 'minecraft:fly_one_cm', 'minecraft:sprint_one_cm',
                         'minecraft:walk_one_cm', 'minecraft:boat_one_cm']
        files = os.scandir(player_dir)
        if not os.stat('totals.json').st_size == 0:
            with open('totals.json') as f:
                content = json.load(f)
                logging = content['logging']
                mining = content['mining']
                farming = content['farming']
                logistics = content['logistics']
                building = content['building']
                crafting = content['crafting']
                fishing = content['fishing']
        for file in files:
            with open(file) as f:
                content = json.load(f)
                building_keys = content['stats']['minecraft:used'].keys()
                crafting_keys = content['stats']['minecraft:crafted'].keys()
                mining_keys = content['stats']['minecraft:mined'].keys()
                for index in logging_arr:
                    if not content['stats']['minecraft:mined'][index] is None:
                        logging = logging + content['stats']['minecraft:mined'][index]
                for index in farming_arr:
                    if not content['stats']['minecraft:mined'][index] is None:
                        farming = farming + content['stats']['minecraft:mined'][index]
                for index in logistics_arr:
                    if not content['stats']['minecraft:custom'][index] is None:
                        logistics = logistics + content['stats']['minecraft:custom'][index]
                if not content['stats']['minecraft:custom']['minecraft:fish_caught'] is None:
                    fishing = fishing + content['stats']['minecraft:custom']['minecraft:fish_caught']
                for key in building_keys:
                    building = building + content['stats']['minecraft:used'][key]
                for key in crafting_keys:
                    crafting = crafting + content['stats']['minecraft:used'][key]
                for key in mining_keys:
                    mining = mining + content['stats']['minecraft:mined'][key]
        result_dict = {'logging': logging, 'mining': mining, 'fishing': fishing, 'crafting': crafting, 'building': building, 'farming': farming, 'logistics': logging}
        with open('totals.json') as f:
            json.dump(result_dict, f)