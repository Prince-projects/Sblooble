import json


class Company:
    def __init__(self, name, funds, industry, description, logo, owner):
        self.name = name
        self.funds = funds
        self.industry = industry
        self.description = description
        self.logo = logo
        self.owner = str(owner)

    def get_stats(self):
        stats = {'Name': self.name, 'Funds': self.funds, 'Industry': self.industry, 'Description': self.description, 'Owner': self.owner}
        return stats

    def get_funds(self):
        return self.funds

    def set_funds(self, new_funds):
        self.funds = new_funds
        return

    def write_stats(self):
        with open('companies/' + str(self.name) + '.json', 'w') as file:
            stats = {'Name': self.name, 'Funds': self.funds, 'Industry': self.industry, 'Description': self.description,
                     'Logo': self.logo, 'Owner': self.owner}
            json.dump(stats, file)
