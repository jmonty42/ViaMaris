class Base:

    def __init__(self, name):
        self.name = name
        # maps of commodity ids to prices for this base
        # what price the player can buy the given commodity from the base at
        self.buy_prices = {}
        # what price the player can sell the given commodity to the base at
        self.sell_prices = {}

    def __str__(self):
        return self.name
