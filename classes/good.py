class Good:

    def __init__(self, name='', price=0.0):
        self.name = name
        self.base_price = price

    def __str__(self):
        return "'" + self.name + "': " + str(self.base_price)