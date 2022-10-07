class Base:
    """
    Represents a base in the game and is used for convenience to keep track of the plugin overrides that the flint API
    doesn't take into account.
    """

    def __init__(self, name, base_id: str = '', system: str = ''):
        self.name = name
        # id of the base
        self.base_id = base_id
        # id of the system the base is in
        self.system = system
        # set of which commodities the player can buy from the base
        self.commodities_to_buy = set()
        # map of commodity ids to prices for this base
        self.commodity_prices = {}

    def __str__(self):
        return self.name + " (" + self.system + ")"
