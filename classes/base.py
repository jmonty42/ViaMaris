class Base:

    def __init__(self, name, nickname='', system=''):
        self.name = name
        # id of the base
        self.nickname = nickname
        # id of the system the base is in
        self.system = system
        # set of which commodities the player can buy from the base
        self.commodities_to_buy = set()
        # map of commodity ids to prices for this base
        self.commodity_prices = {}

    def __str__(self):
        return self.name + " (" + self.system + ")"
