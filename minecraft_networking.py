import json

from mctools import RCONClient

HOST = 'localhost'  # Hostname of the Minecraft server
PORT = 25575  # Port number of the RCON server
rcon = RCONClient(HOST, port=PORT)


def load_creds():
    with open('creds.json') as f:
        content = json.load(f)
        return content['rcon']


class MinecraftNetworking:
    def __init__(self, target, item, amount):
        self.item = item
        self.target = target
        self.amount = amount

    def buy_command(self):
        if rcon.login(load_creds()):
            print('give ' + self.target + ' ' + self.item + ' ' + str(self.amount))
            rcon.command('give ' + self.target + ' ' + self.item + ' ' + str(self.amount))
            print('yip')
