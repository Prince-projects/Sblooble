import json
import math
import os
import random


class CompanyEvent:

    def event_generator(self, industry, effect):
        file_names = []
        if effect == "positive":
            files = os.scandir("positiveevents")
            open_dir = 'positiveevents'
        if effect == "negative":
            files = os.scandir("negativeevents")
            open_dir = 'negativeevents'
        for file in files:
            if industry in file.name:
                file_names.append(file.name)
        index = random.randint(0, len(file_names) - 1)
        with open(open_dir + '/' + file_names[index]) as f:
            content = json.load(f)
            result = {'message': content['message'], 'effect': effect, 'industry': industry}
            return result

    def mod_funds(self, rate, effect, industry):
        files = os.scandir('companies')
        with open('boosts.json') as f:
            boost_content = json.load(f)
        for file in files:
            with open(file) as f:
                content = json.load(f)
                if content['Industry'] == industry:
                    funds = content['Funds']
                    mod_amount = math.floor(funds * (rate / 100))
                    if effect == 'positive':
                        content['Funds'] = content['Funds'] + mod_amount + boost_content[industry]
                        boost_content[industry] = 0
                    if effect == 'negative':
                        content['Funds'] = content['Funds'] - mod_amount + boost_content[industry]
                        boost_content[industry] = 0
                    with open('boosts.json', 'w') as boost_file:
                        json.dump(boost_content, boost_file)
                with open(file, 'w') as content_f:
                    json.dump(content, content_f)


    def company_cleanup(self):
        remove = False
        files = os.scandir('companies')
        for file in files:
            with open(file) as f:
                content = json.load(f)
                if content['Funds'] <= 0:
                    remove = True
            if remove:
                os.remove(file)
                return 'cleaned'
            remove = False

    def calc_boosts(self, difference_dict):
        old_content = {}
        print("Writing Boosts...")
        if not os.stat('boosts.json').st_size == 0:
            with open('boosts.json') as f:
                old_content = json.load(f)
        logging_boost = 0
        logi_boost = 0
        crafting_boost = 0
        farming_boost = 0
        mining_boost = 0
        fishing_boost = 0
        building_boost = 0
        if difference_dict['mining'] > 20000:
            mining_boost = math.ceil(difference_dict['mining'] / 20000)
            if not os.stat('boosts.json').st_size == 0:
                if old_content['mining'] > mining_boost:
                    mining_boost = old_content['mining']
        if difference_dict['logging'] > 1500:
            logging_boost = math.ceil(difference_dict['logging'] / 1500)
            if not os.stat('boosts.json').st_size == 0:
                if old_content['logging'] > logging_boost:
                    logging_boost = old_content['logging']
        if difference_dict['logistics'] > 15000:
            logi_boost = math.ceil(difference_dict['logistics'] / 15000)
            if not os.stat('boosts.json').st_size == 0:
                if old_content['logistics'] > logi_boost:
                    logi_boost = old_content['logistics']
        if difference_dict['farming'] > 15000:
            farming_boost = math.ceil(difference_dict['farming'] / 15000)
            if not os.stat('boosts.json').st_size == 0:
                if old_content['farming'] > farming_boost:
                    farming_boost = old_content['farming']
        if difference_dict['crafting'] > 10000:
            crafting_boost = math.ceil(difference_dict['crafting'] / 10000)
            if not os.stat('boosts.json').st_size == 0:
                if old_content['crafting'] > crafting_boost:
                    crafting_boost = old_content['crafting']
        if difference_dict['building'] > 10000:
            building_boost = math.ceil(difference_dict['building'] / 10000)
            if not os.stat('boosts.json').st_size == 0:
                if old_content['building'] > building_boost:
                    building_boost = old_content['building']
        if difference_dict['fishing'] > 80:
            fishing_boost = math.ceil(difference_dict['fishing'] / 80)
            if not os.stat('boosts.json').st_size == 0:
                if old_content['fishing'] > fishing_boost:
                    fishing_boost = old_content['fishing']
        boost_dict = {'fishing': fishing_boost, 'building': building_boost, 'crafting': crafting_boost,
                      'farming': farming_boost, 'logistics': logi_boost, 'logging': logging_boost,
                      'mining': mining_boost}
        with open('boosts.json', 'w') as f:
            json.dump(boost_dict, f)
