import json
import discord
from discord import app_commands
from discord import interactions

import company
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

    @tree.command(name="registercompany", description="Command to register a company.")
    async def register_company(self, interaction: interactions, name, funds, industry, description, logo):
        user_company = company.Company(name, funds, industry, description, logo)
        user_company.write_stats()
        await interaction.response.send_message(content="Company created with the following info: " + user_company.get_stats())

    @tree.command(name="registeraccount", description="Command to register an account")
    async def register_account(self, interaction: interactions):
        user_id = interaction.User.id
        await interaction.response.send_message(content=user_id)

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
