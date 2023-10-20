import json
import os

import requests
from mojang import API

api = API()
player_dir = '/home/karl/CelestialVanilla/world/stats/'


class PlayerStats:

    def __init__(self, player, param1, param2):
        self.player = player
        self.param1 = param1
        self.param2 = param2

    def get_all_players(self):
        players = os.scandir(player_dir)
        player_arr = []
        for player in players:
            if player.name is not None:
                cleaned = player.name.replace('.json', ' ')
                cleaned_2 = cleaned.replace('-', '')
                cleaned_3 = cleaned_2.replace(' ', '')
                name = api.get_username(cleaned_3)
                player_arr.append(name)
        return player_arr

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
        industry_array = ['logging', 'mining', 'logistics', 'fishing', 'farming', 'crafting', 'building']
        difference_dict = {}
        player_difference_dict = {}
        player_dict = {}
        logistics = 0
        building = 0
        mining = 0
        logging = 0
        crafting = 0
        fishing = 0
        farming = 0
        logging_arr = ['minecraft:oak_log', 'minecraft:birch_log', 'minecraft:spruce_log', 'minecraft:acacia_log',
                       'minecraft:jungle_log', 'minecraft:mangrove_log', 'minecraft:dark_oak_log',
                       'minecraft:cherry_log']
        farming_arr = ['minecraft:wheat', 'minecraft:kelp', 'minecraft:sugar_cane', 'minecraft:potatoes',
                       'minecraft:bamboo', 'minecraft:beetroots', 'minecraft:carrots', 'minecraft:sweet_berry_bush']
        logistics_arr = ['minecraft:swim_one_cm', 'minecraft:fly_one_cm', 'minecraft:sprint_one_cm',
                         'minecraft:walk_one_cm', 'minecraft:boat_one_cm']
        files = os.scandir(player_dir)
        if not os.stat('totals.json').st_size == 0:
            with open('totals.json') as f:
                previous_content = json.load(f)
        if not os.stat('individual_contributions.json').st_size == 0:
            with open('individual_contributions.json') as f:
                previous_player = json.load(f)
        for file in files:
            player_logistics = 0
            player_building = 0
            player_mining = 0
            player_logging = 0
            player_crafting = 0
            player_fishing = 0
            player_farming = 0
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
                            player_logging = player_logging + content['stats']['minecraft:mined'][index]
                if not content['stats'].get('minecraft:mined') is None:
                    for index in farming_arr:
                        if not content['stats']['minecraft:mined'].get(index) is None:
                            farming = farming + content['stats']['minecraft:mined'][index]
                            player_farming = player_logging + content['stats']['minecraft:mined'][index]
                if not content['stats'].get('minecraft:custom') is None:
                    for index in logistics_arr:
                        if not content['stats']['minecraft:custom'].get(index) is None:
                            logistics = logistics + content['stats']['minecraft:custom'][index]
                            player_logistics = player_logistics + content['stats']['minecraft:custom'][index]
                if not content['stats'].get('minecraft:custom') is None:
                    if not content['stats']['minecraft:custom'].get('minecraft:fish_caught') is None:
                        fishing = fishing + content['stats']['minecraft:custom']['minecraft:fish_caught']
                        player_fishing = player_fishing + content['stats']['minecraft:custom']['minecraft:fish_caught']
                if not content['stats'].get('minecraft:used') is None:
                    for key in building_keys:
                        building = building + content['stats']['minecraft:used'][key]
                        player_building = player_building + content['stats']['minecraft:used'][key]
                if not content['stats'].get('minecraft:crafted') is None:
                    for key in crafting_keys:
                        crafting = crafting + content['stats']['minecraft:crafted'][key]
                        player_crafting = player_crafting + content['stats']['minecraft:crafted'][key]
                if not content['stats'].get('minecraft:used') is None:
                    for key in mining_keys:
                        mining = mining + content['stats']['minecraft:mined'][key]
                        player_mining = player_mining + content['stats']['minecraft:mined'][key]
            sub_dict = {'logging': player_logging, 'mining': player_mining, 'fishing': player_fishing,
                        'crafting': player_crafting,
                        'building': player_building, 'farming': player_farming, 'logistics': player_logistics}
            player_dict[file.name] = sub_dict
        building = building - mining
        mining = mining - logging
        result_dict = {'logging': logging, 'mining': mining, 'fishing': fishing, 'crafting': crafting,
                       'building': building, 'farming': farming, 'logistics': logistics / 100}
        with open('totals.json', 'w') as f:
            json.dump(result_dict, f)
        with open('totals.json') as f:
            current_content = json.load(f)
        for item in previous_content:
            item_diff = current_content[item] - previous_content[item]
            difference_dict[item] = item_diff
        with open('individual_contributions.json') as f:
            for item in previous_player:
                player_difference_dict[item] = {}
                for x in industry_array:
                    item_diff = player_dict[item][x] - previous_player[item][x]
                    player_difference_dict[item][x] = item_diff
        with open('player_difference.json', 'w') as f:
            print('Difference Dict: ', difference_dict)
            json.dump(player_difference_dict, f)
        with open('individual_contributions.json', 'w') as f:
            json.dump(player_dict, f)
        return difference_dict
