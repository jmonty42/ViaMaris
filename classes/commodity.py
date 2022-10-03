from classes.pricelist import PriceList


class Commodity:

    def __init__(self, name, price=0.0):
        self.name = name
        self.base_price = price
        self.best_buy_prices = PriceList(least_first=True)
        self.best_sell_prices = PriceList()

    def __str__(self):
        return "'" + self.name + "': " + str(self.base_price)
