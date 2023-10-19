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

    def mod_funds(self, rate, effect):
        files = os.scandir('companies')
        for file in files:
            with open(file) as f:
                content = json.load(f)
                funds = content['Funds']
                mod_amount = math.floor(funds * (rate / 100))
                if effect == 'positive':
                    content['Funds'] = content['Funds'] + mod_amount
                if effect == 'negative':
                    content['Funds'] = content['Funds'] - mod_amount
            with open(file, 'w') as f:
                json.dump(content, f)

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
