from mctools import RCONClient

HOST = 'mc.server.net'  # Hostname of the Minecraft server
PORT = 25575  # Port number of the RCON server
rcon = RCONClient(HOST, port=PORT)

class MinecraftNetworking:
    def __init__(self, target, item, amount):
        self.item = item
        self.target = target
        self.amount = amount

    def buy_command(self):
        if rcon.login():
            print('give ' + self.target + ' ' + self.item + ' ' + str(self.amount))
            rcon.command('give ' + self.target + ' ' + self.item + ' ' + str(self.amount))