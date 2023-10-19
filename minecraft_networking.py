import json
import os

from mojang import API
from mctools import RCONClient

import player_stats

HOST = 'localhost'  # Hostname of the Minecraft server
PORT = 25575  # Port number of the RCON server
rcon = RCONClient(HOST, port=PORT)
api = API()


def load_creds():
    with open('creds.json') as f:
        content = json.load(f)
        return content['rcon']


class MinecraftNetworking:
    def __init__(self, target, item, amount):
        self.item = item
        self.target = target
        self.amount = amount

    def player_online(self):
        if rcon.login(load_creds()):
            players = rcon.command('list')
            if self.target not in players:
                return False
            return True

    def send_codes(self):
        if rcon.login(load_creds()):
            stats = player_stats.PlayerStats(None, None, None)
            players_list = stats.get_all_players()
            print(players_list)
            players = rcon.command('list')
            print(players)
            for player in players_list:
                uuid = api.get_uuid(player)
                files = os.scandir('cashcodes/')
                print(uuid)
                for file in files:
                    if uuid in file.name:
                        with open(file) as f:
                            content = json.load(f)
                            message = 'Your codes remaining are: ' + str(content.keys())
                            print(message)
                            cmd = rcon.command('tell ' + player + ' ' + message)
                            print(cmd)

    def buy_command(self):
        if not self.player_online():
            return False
        if rcon.login(load_creds()):
            rcon.command('give ' + self.target + ' ' + self.item + ' ' + str(self.amount))
            return True
