import json
import os


class CompanyEvent:
    def __init__(self, industry, variable_rate, description):
        self.industry = industry
        self.variable_rate = variable_rate
        self.description = description

    async def company_cleanup(self):
        files = os.scandir('companies')
        for file in files:
            with open(file) as f:
                content = json.load(f)
                if content['funds'] <= 0:
                    os.remove(file)
