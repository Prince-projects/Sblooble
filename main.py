import json
import discord
from discord import app_commands
from discord import interactions
import player_stats

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)  # A tree of slash commands for the bot.


def load_creds():
    with open("creds.json") as f:
        content = json.load(f)
        return content['token']


class SbloobleBot:

    @tree.command(name="statsguide", description="A guide for the stats command")
    async def stats_guide(self, interaction: interactions):
        await interaction.response.send_message(content='See this pastebin for help: '
                                                        'https://pastebin.com/hQXbzPS5')

    @tree.command(name="stats", description="A statistics command for Celestial's Dew.")
    async def stats_guide(self, interaction: interactions, player: str, param1: str, param2: str):
        stats = player_stats.PlayerStats(player, param1, param2)
        result = await stats.find_stats()
        await interaction.response.send_message(content='Parameter: ' + param2 + '. ' + 'Result: ' + str(result))

    @client.event
    async def on_ready(self):
        await tree.sync()
        print(f'Logged in as {client.user}')

    @client.event
    async def on_message(self, message):
        if message.author == client.user:
            return


client.run(load_creds())
print('epico')
