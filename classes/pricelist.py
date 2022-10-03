class PriceNode:

    def __init__(self, price, base):
        self.price = price
        self.base = base
        self.next: PriceNode = None


class PriceList:

    def __init__(self, least_first=False, max_length=10):
        self.top: PriceNode = None
        self.bottom: PriceNode = None
        self.least_first: bool = least_first
        self.length: int = 0
        self.max_length: int = max_length

    def add_price(self, price, base):
        should_add = False
        if self.length < self.max_length:
            should_add = True
        elif (self.bottom.price > price and self.least_first) or \
                (self.bottom.price < price and not self.least_first):
            should_add = True

        if should_add:
            new_node = PriceNode(price, base)
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
