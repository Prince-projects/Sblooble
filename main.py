import math
from datetime import datetime

from discord.ext import tasks
import json
import random

import discord
from discord import app_commands
from discord import interactions
import os

import company
import minecraft_networking
import player_stats
import company_event

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)  # A tree of slash commands for the bot.


# Add indents to each json dump
# Add a refresh command for the tree sync to avoid blacklisting
# Add a redeem ability to the bot, so you can redeem codes you get

def load_creds():
    with open("creds.json") as f:
        content = json.load(f)
        return content['token']


def get_total_wealth():
    company_funds = []
    user_funds = []
    companies = os.scandir('companies')
    users = os.scandir('users')
    for company in companies:
        with open(company) as f:
            content = json.load(f)
            company_funds.append(content['Funds'])
    for user in users:
        with open(user) as f:
            content = json.load(f)
            user_funds.append(content['funds'])
    return sum(user_funds) + sum(company_funds)


def company_exists(tested_company):
    exists = False
    existing = os.scandir('companies')
    for exist in existing:
        if exist.name == tested_company + '.json':
            exists = True
    if not exists:
        return 'no'


def user_exists(user):
    exists = False
    existing = os.scandir('users')
    for exist in existing:
        if exist.name == user + '.json':
            exists = True
    if not exists:
        return 'no'


def calc_item_price(item):
    with open('price_list.json') as f:
        content = json.load(f)
        keys = content.keys()
        for key in keys:
            if item == key:
                result = content[key]
        price = math.floor(get_total_wealth() * result)
        return price


# random.randint(60, 240)
# @tasks.loop(minutes=60) - UNCOMMENT BEFORE PSUHING TO PROD ****************************************************************************************************************************************
async def generate_event():
    dt = datetime.today()
    industry_array = ['logging', 'mining', 'logistics', 'fishing', 'farming', 'crafting', 'building']
    effect_array = ['positive', 'negative']
    mod_rand = random.randint(0, 20)
    industry_rand = random.randint(0, len(industry_array) - 1)
    effect_rand = random.randint(0, 1)
    event = company_event.CompanyEvent()
    if not event.company_cleanup() == 'cleaned':
        event_content = event.event_generator(industry_array[industry_rand], effect_array[effect_rand])
        event.mod_funds(mod_rand, effect_array[effect_rand])
        result = {math.floor(dt.timestamp()): {'message': event_content['message'],
                                               'industry': event_content['industry'],
                                               'effect': event_content['effect'], 'rate': str(mod_rand)}}
        if not os.stat("event_history.json").st_size == 0:
            with open("event_history.json", 'r') as file:
                content = json.load(file)
            with open("event_history.json", 'w') as file:
                content.update(result)
                json.dump(content, file)
        else:
            with open("event_history.json", 'w') as file:
                json.dump(result, file)

@tasks.loop(minutes=random.randint(60, 300))
async def generate_cash_code():
    return
    # Get list of online players
    # Get stats of all players for a few industries (fish caught, logs chopped, distance walked, etc.)
    # select one at random
    # get top breaker, 50% chance it's them, rest of the chance is split between the rest. top 5 only if roll is 5+ to top, 2nd is 25%, 12.5% 3rd, 4/5th is 6.25%

@tree.command(name="companyeventhistory", description="A command to check event history")
async def event_history(interaction: interactions):
    events = ''
    with open("event_history.json") as f:
        content = json.load(f)
        keys = content.keys()
        sorted_keys = sorted(keys, reverse=True)
        for x in range(5):
            events = events + '`' + content[sorted_keys[x]]['message'] + ' Affected industry: ' + \
                     content[sorted_keys[x]]['industry'] + '. An overall **' + content[sorted_keys[x]][
                         'effect'] + '** outcome! Valuation affected by ' + content[sorted_keys[x]][
                         'rate'] + '%!' + '`' + '\n'
    await interaction.response.send_message(
        content=events)


@tree.command(name="playerstatsguide", description="A guide for the stats command")
async def player_stats_guide(interaction: interactions):
    await interaction.response.send_message(content='See this pastebin for help: '
                                                    'https://pastebin.com/hQXbzPS5')


# Need to deduct user funds
@tree.command(name="companyregister", description="Command to register a company.")
@app_commands.choices(
    industry=[
        app_commands.Choice(name="logging", value='logging'),
        app_commands.Choice(name="mining", value='mining'),
        app_commands.Choice(name="building", value='building'),
        app_commands.Choice(name="fishing", value='fishing'),
        app_commands.Choice(name="logistics", value='logistics'),
        app_commands.Choice(name="crafting", value='crafting'),
        app_commands.Choice(name="farming", value='farming'),
    ]
)
async def company_register(interaction: interactions, name: str, funds: float, industry: app_commands.Choice[str],
                           description: str, logo: str):
    if user_exists(str(interaction.user)) == 'no':
        await interaction.response.send_message(content='Make sure you register an account first!')
        return
    if funds < 1:
        await interaction.response.send_message(content='Allocate funds to the company. PLEASE.')
        return
    industry_array = ['logging', 'mining', 'logistics', 'fishing', 'farming', 'crafting', 'building']
    with open('users/' + str(interaction.user) + '.json') as file:
        content = json.load(file)
        user_funds = content['funds']
    if user_funds < funds:
        await interaction.response.send_message(content='Not enough funds!')
        return
    if industry.value not in industry_array:
        await interaction.response.send_message(content='Bad Industry! Ensure correct industry setting.')
    user_company = company.Company(name, funds, industry.value, description, logo, interaction.user)
    user_company.write_stats()
    with open('users/' + str(interaction.user) + '.json', 'w') as f:
        content['funds'] = content['funds'] - funds
        json.dump(content, f)
    await interaction.response.send_message(content='Company created!')


@tree.command(name="accountregister", description="Command to register an account")
async def account_register(interaction: interactions):
    user_id = str(interaction.user)
    users = os.scandir('users')
    for single_user in users:
        if str(user_id) in single_user.name:
            await interaction.response.send_message(content='User already created!')
            return
    with open('users/' + user_id + '.json', 'w') as f:
        user_dict = {'user': user_id, 'funds': 100}
        json.dump(user_dict, f)
        await interaction.response.send_message(content='Account ' + user_id + ' created!')
    if len(os.listdir('users/')) == 0:  # If no users in directory, loop will not run, so we have a catch here.
        with open('users/' + user_id + '.json', 'w') as f:
            user_dict = {'user': user_id, 'funds': 100}
            json.dump(user_dict, f)
            await interaction.response.send_message(content='Account ' + user_id + ' created!')


@tree.command(name="accountinfo", description="Command to check someone's account info")
async def account_info(interaction: interactions, player: str):
    users = os.scandir('users')
    for single_user in users:
        if player in single_user.name:
            with open('users/' + player + '.json') as f:
                content = json.load(f)
                await interaction.response.send_message(
                    content='Account found! Name: ' + content['user'] + ', Funds remaining: ' + str(
                        content['funds']) + '.')
                return
    await interaction.response.send_message(content='Invalid user, or user not registered!')


@tree.command(name="companyinfo", description="Command to check the information of a company")
async def company_info(interaction: interactions, desired_company: str):
    if company_exists(desired_company) == 'no':
        await interaction.response.send_message(content='No company found.')
        return
    with open('companies/' + desired_company + '.json') as file:
        content = json.load(file)
    await interaction.response.send_message(
        content='Company found!' + '\n' + '`Name: ' + content['Name'] + '`\n' + '`Funds: ' +
                str(content['Funds']) + '`\n' + '`Industry: ' + content['Industry'] +
                '`\n' + '`Description: ' + content['Description'] + '`\n' +
                '`Logo Link: ' + content['Logo'] + '`\n' + '`Owner: ' +
                content['Owner'] + '`')


@tree.command(name="companylist", description="Command to check the list of companies")
async def company_list(interaction: interactions):
    file_names = []
    result = 'Company Directories: '
    files = os.scandir('companies')
    for file in files:
        new = file.name.replace('.json', '')
        file_names.append(new)
    for entry in file_names:
        result = result + entry + ', '
    await interaction.response.send_message(content=result)


@tree.command(name="itemprice", description="Command to check the list of item prices")
async def item_price(interaction: interactions, item: str):
    price = calc_item_price(item)
    await interaction.response.send_message(content=str(item) + ', Price: ' + str(price))


@tree.command(name="playerstats", description="A statistics command for Celestial's Dew.")
async def player_stats(interaction: interactions, player: str, param1: str, param2: str):
    stats = player_stats.PlayerStats(player, param1, param2)
    result = await stats.find_stats()
    await interaction.response.send_message(content='Parameter: ' + param2 + '. ' + 'Result: ' + str(result))


@tree.command(name="refresh", description="OWNER command to refresh command trees")
async def refresh(interaction: interactions):
    if str(interaction.user) == 'princecord':
        await tree.sync()
        await interaction.response.send_message(
            content='Refreshed tree commands. Some text to make it seem mystical and '
                    'developer-e. TIME=9291, CODE=PUR21, ERRNO=NONE, FLEEPORGLORB=YEP YEP')
    else:
        await interaction.response.send_message(
            content='You are NOT the owner... event grabbed, reported, stored, snacked on, consumed, ingested. he '
                    'WILL be made aware.')


@tree.command(name="companywithdraw", description="A command to withdraw funds from a company you own.")
async def company_withdraw(interaction: interactions, withdraw_amount: float, desired_company: str):
    if user_exists(str(interaction.user)) == 'no':
        await interaction.response.send_message(content='Make sure you register an account first!')
        return
    if company_exists(desired_company) == 'no':
        await interaction.response.send_message(content='No company found.')
        return
    with open('companies/' + desired_company + '.json') as file:
        content = json.load(file)
        if content['Funds'] < withdraw_amount:
            await interaction.response.send_message(content='Not enough funds in company account!')
            return
        if not content['Owner'] == str(interaction.user):
            await interaction.response.send_message(content='Not your company')
            return
    with open('companies/' + desired_company + '.json', 'w') as file:
        content['Funds'] = content['Funds'] - withdraw_amount
        json.dump(content, file)
    with open('users/' + str(interaction.user) + '.json', 'r') as userfile:
        user_content = json.load(userfile)
    with open('users/' + str(interaction.user) + '.json', 'w') as userfile:
        user_content['funds'] = user_content['funds'] + withdraw_amount
        json.dump(user_content, userfile)
    await interaction.response.send_message(content='Withdraw Successful!')


@tree.command(name="companydeposit", description="A command to deposit funds from a company you own.")
async def company_deposit(interaction: interactions, deposit_amount: float, desired_company: str):
    if user_exists(str(interaction.user)) == 'no':
        await interaction.response.send_message(content='Make sure you register an account first!')
        return
    if company_exists(desired_company) == 'no':
        await interaction.response.send_message(content='No company found.')
        return
    with open('companies/' + desired_company + '.json') as file:
        content = json.load(file)
        if not content['Owner'] == str(interaction.user):
            await interaction.response.send_message(content='Not your company')
            return
    with open('users/' + str(interaction.user) + '.json', 'r') as userfile:
        user_content = json.load(userfile)
    with open('users/' + str(interaction.user) + '.json', 'w') as userfile:
        user_content['funds'] = user_content['funds'] - deposit_amount
        json.dump(user_content, userfile)
    with open('companies/' + desired_company + '.json', 'w') as file:
        content['Funds'] = content['Funds'] + deposit_amount
        json.dump(content, file)
    await interaction.response.send_message(content='Deposit Successful!')


@tree.command(name="itembuy", description="A command to buy items")
async def item_buy(interaction: interactions, target: str, item: str, amount: int):
    if user_exists(str(interaction.user)) == 'no':
        await interaction.response.send_message(content='Make sure you register an account first!')
        return
    item_price_individual = calc_item_price(item)
    with open('users/' + str(interaction.user) + '.json', 'r') as userfile:
        user_content = json.load(userfile)
    if float(user_content['funds']) < item_price_individual * amount:
        await interaction.response.send_message(content='Not enough funds!')
        return
    with open('users/' + str(interaction.user) + '.json', 'w') as userfile:
        user_content['funds'] = user_content['funds'] - (item_price_individual * amount)
        json.dump(user_content, userfile)
    server = minecraft_networking.MinecraftNetworking(target, item, amount)
    if not server.buy_command():
        await interaction.response.send_message(content='Player not online!')
    else:
        await interaction.response.send_message(content='Buy Successful!')


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
    if "positiveevents" not in names:
        os.mkdir('positiveevents')
    if "negativeevents" not in names:
        os.mkdir('negativeevents')
    if 'event_history.json' not in names:
        with open('event_history.json', 'w') as f:
            pass
    if 'price_list.json' not in names:
        with open('price_list.json', 'w') as f:
            pass
    # generate_event.start() *************************************************************** UNCOMMENT b4 PROD
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return


client.run(load_creds())
