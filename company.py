class Company:
    def __init__(self, name, funds, industry, description, logo):
        self.name = name
        self.funds = funds
        self.industry = industry
        self.description = description
        self.logo = logo

    def get_stats(self):
        stats = {'Name': self.name, 'Funds': self.funds, 'Industry': self.industry, 'Description': self.description}
        return stats

    def get_funds(self):
        return self.funds

    def set_funds(self, new_funds):
        self.funds = new_funds
        return
