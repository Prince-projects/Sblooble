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


@tree.command(name="companyregister", description="Command to register a company.")
async def companyregister(interaction: interactions, name: str, funds: float, industry: str,
                          description: str, logo: str):
    industry_array = ['Logging', 'Mining', 'Logistics', 'Fishing', 'Farming', 'Crafting', 'Building']
    with open('users/' + str(interaction.user) + '.json') as file:
        print('1')
        content = json.load(file)
        user_funds = content['funds']
    if user_funds < funds:
        print('2')
        await interaction.response.send_message(content='Not enough funds!')
        return
    if industry not in industry_array:
        print('3')
        await interaction.response.send_message(content='Bad Industry! Ensure correct industry setting.')
    print('4')
    user_company = company.Company(name, funds, industry, description, logo, interaction.user)
    user_company.write_stats()
    await interaction.response.send_message(content='Company created!')


@tree.command(name="registeraccount", description="Command to register an account")
async def register_account(interaction: interactions):
    user_id = str(interaction.user)
    users = os.scandir('users')
    for single_user in users:
        if str(user_id) in single_user.name:
            await interaction.response.send_message(content='User already created!')
            return
        with open('users/' + user_id + '.json', 'w') as f:
            user_dict = {'user': user_id, 'funds': 0}
            json.dump(user_dict, f)
            await interaction.response.send_message(content='Account ' + user_id + ' created!')
    if len(os.listdir('users')) == 0:
        with open('users/' + user_id + '.json', 'w') as f:
            user_dict = {'user': user_id, 'funds': 0}
            json.dump(user_dict, f)
            await interaction.response.send_message(content='Account ' + user_id + ' created!')


@tree.command(name="companyinfo", description="Command to check the information of a company")
async def company_info(interaction: interactions, desired_company: str):
    with open('companies/' + desired_company + '.json') as file:
        f = json.load(file)
        stats = {'Name': f['Name'], 'Funds': f['Funds'], 'Industry': f['Industry'], 'Description': f['Description'],
                 'Logo': f['Logo'], 'Owner': f['Owner']}
    await interaction.response.send_message(content=str(stats))


@tree.command(name="companylist", description="Command to check the list of companies")
async def company_list(interaction: interactions):
    file_names = []
    files = os.scandir('companies')
    for file in files:
        file_names.append(file.name)
    await interaction.response.send_message(content=str(file_names))


@tree.command(name="playerstats", description="A statistics command for Celestial's Dew.")
async def player_stats(interaction: interactions, player: str, param1: str, param2: str):
    stats = player_stats.PlayerStats(player, param1, param2)
    result = await stats.find_stats()
    await interaction.response.send_message(content='Parameter: ' + param2 + '. ' + 'Result: ' + str(result))


@tree.command(name="companywithdraw", description="A command to withdraw funds from a company you own.")
async def company_withdraw(interaction: interactions, withdraw_amount: float, desired_company: str):
    with open(desired_company + '.json') as file:
        content = json.load(file)
        if content['Funds'] < withdraw_amount:
            await interaction.response.send_message(content='Not enough funds in company account!')
            return
        if content['Owner'] != interaction.user:
            await interaction.response.send_message(content='Not your company')
            return
        content['Funds'] = content['Funds'] - withdraw_amount
        json.dump(content, file)
    with open('users/' + interaction.user + '.json') as userfile:
        content = json.load(userfile)
        content['funds'] = content['funds'] + withdraw_amount
        json.dump(content, userfile)
    await interaction.response.send_message(content='')


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
