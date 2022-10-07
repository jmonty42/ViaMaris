from classes.pricelist import PriceList


class Commodity:
    """
    This represents a sellable Commodity in the game and keeps track of the best bases to buy and sell that commodity.
    """

    def __init__(self, name, price=0):
        self.name = name
        self.default_price = price
        self.price_map = {}
        # A sorted list of base ids where the player can buy the commodity for the best price
        self.best_buy_prices = PriceList(least_first=True)
        # A sorted list of base ids where the player can sell the commodity for the best price
        self.best_sell_prices = PriceList()
        self.volume = 0

    def __str__(self):
        return "'" + self.name + "': " + str(self.default_price)
