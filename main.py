import json
import discord
from discord import app_commands
from discord import interactions
import os

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


@tree.command(name="statsguide", description="A guide for the stats command")
async def stats_guide(interaction: interactions):
    await interaction.response.send_message(content='See this pastebin for help: '
                                                    'https://pastebin.com/hQXbzPS5')


@tree.command(name="registercompany", description="Command to register a company.")
async def register_company(interaction: interactions, name: str, funds: float, industry: str,
                           description: str, logo: str):
    with open('users/' + str(interaction.user) + '.json') as file:
        content = json.load(file)
        user_funds = content['funds']
    if user_funds < funds:
        await interaction.response.send_message(content='Not enough funds!')
        return
    user_company = company.Company(name, funds, industry, description, logo, interaction.user)
    user_company.write_stats()
    await interaction.response.send_message(content='Company created!')


@tree.command(name="registeraccount", description="Command to register an account")
async def register_account(interaction: interactions):
    user_id = interaction.user
    if user_id in os.scandir('users/'):
        return await interaction.response.send_message(content='User already created!')
    else:
        with open('users/' + str(user_id) + '.json', 'w') as f:
            user_dict = {'user': str(user_id), 'funds': 0}
            json.dump(user_dict, f)
            await interaction.response.send_message(content=user_id)


@tree.command(name="stats", description="A statistics command for Celestial's Dew.")
async def stats_guide(interaction: interactions, player: str, param1: str, param2: str):
    stats = player_stats.PlayerStats(player, param1, param2)
    result = await stats.find_stats()
    await interaction.response.send_message(content='Parameter: ' + param2 + '. ' + 'Result: ' + str(result))


@client.event
async def on_ready():
    files = os.scandir('.')
    names = []
    for file in files:
        names.append(file.name)
    if "users" not in names:
        os.mkdir('users')
    if "companies" not in names:
        os.mkdir('companies')
    await tree.sync()
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return


client.run(load_creds())
