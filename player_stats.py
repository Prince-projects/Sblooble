import json
from mojang import API
import os

api = API()
player_dir = '/home/karl/CelestialVanilla/world/stats/'


# https://pastebin.com/hQXbzPS5
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
