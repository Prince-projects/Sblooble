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
        message = ''
        if rcon.login(load_creds()):
            stats = player_stats.PlayerStats(None, None, None)
            players_list = stats.get_all_players()
            players = rcon.command('list')
            for player in players_list:
                if player in players:
                    uuid = api.get_uuid(player)
                    files = os.scandir('cashcodes/')
                    for file in files:
                        new_name = file.name.replace('-', '')
                        if uuid in new_name:
                            with open(file) as f:
                                content = json.load(f)
                                if len(content.keys()) > 0:
                                    for x in content.keys():
                                        message = message + ' ' + x
                                    player_message = 'Your codes remaining are: ' + message + '.' + ('You can use the '
                                                                                                     'ATLauncher '
                                                                                                     'console or the '
                                                                                                     'minecraft '
                                                                                                     'console that '
                                                                                                     'opens alongside '
                                                                                                     'your game to '
                                                                                                     'copy paste, '
                                                                                                     'and redeem them '
                                                                                                     'via the bot!')
                                    cmd = rcon.command('tell ' + player + ' ' + player_message)

    def buy_command(self):
        if not self.player_online():
            return False
        if rcon.login(load_creds()):
            rcon.command('give ' + self.target + ' ' + self.item + ' ' + str(self.amount))
            return True
