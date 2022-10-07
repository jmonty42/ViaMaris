class PriceNode:

    def __init__(self, price, string_id):
        self.price = price
        self.string_id = string_id
        self.next: PriceNode = None


class PriceList:
    """
    A sorted list of prices with associated string ids. The list can either be sorted least first or greatest first.

    Each Commodity will have a PriceList with base ids representing which bases have the lowest buy price (meaning the
    player will pay the least amount of credits to buy that commodity from that base) and another PriceList representing
    which bases have the highest sell price (meaning the player will receive the most amount of credits when selling the
    commodity to that base).
    """

    def __init__(self, least_first: bool = False, max_length: int = 10):
        """
        Returns an empty PriceList with the default sorting to greatest first and the max length of 10.
        :param least_first: bool
        :param max_length: int
        """
        self.top: PriceNode = None
        self.bottom: PriceNode = None
        self.least_first: bool = least_first
        self.length: int = 0
        self.max_length: int = max_length

    def add_price(self, price, string_id):
        """
        Given a price, string_id pair, this method will determine if it should be added to the list.
        :param price:
        :param string_id:
        :return:
        """
        should_add = False
        if self.length < self.max_length:
            should_add = True
        elif (self.bottom.price > price and self.least_first) or \
                (self.bottom.price < price and not self.least_first):
            should_add = True

        if should_add:
            new_node = PriceNode(price, string_id)
            if self.length == 0:
                # the list is empty
                self.top = new_node
                self.bottom = new_node
                self.length += 1
                return
            else:
                # start at the top
                current_node = self.top
                while current_node.next and \
                        ((self.least_first and current_node.next.price < new_node.price) or
                         (not self.least_first and current_node.next.price > new_node.price)):
                    # new node should go after the current node
                    current_node = current_node.next
                if current_node == self.top and \
                        ((self.least_first and current_node.price > new_node.price) or
                         (not self.least_first and current_node.price < new_node.price)):
                    # new node should go before the top node
                    self.top = new_node
                    new_node.next = current_node
                    current_node = new_node
                else:
                    # new node should go right after the current node (after traversing the loop above)
                    new_node.next = current_node.next
                    current_node.next = new_node
                if new_node.next is None:
                    # the current_node was the last node in the list
                    self.bottom = new_node
                    self.length += 1
                else:
                    if self.length == self.max_length:
                        # need to remove the last element
                        # when current_node.next.next is None, current_node is the new last node
                        while current_node.next.next:
                            current_node = current_node.next
                        self.bottom = current_node
                        current_node.next = None
                    else:
                        self.length += 1
