"""
Order model
Order is basically a list of ordered packages
"""

class Order:
    def __init__(self, item_orders={}):
        self.item_orders = item_orders

    def get_order(self, item):
        return self.item_orders.get(item, 0)

    def add_to_order(self, item, quantity):
        self.item_orders[item] = self.item_orders.get(item, 0) + quantity

    def remove_from_order(self, item, quantity):
        if quantity > self.item_orders.get((item, 0)):
            raise Exception("Order doesn't need this much quantity")
        self.item_orders[item] = self.item_orders.get(item, 0) - quantity

    def __iter__(self):
        return iter(self.item_orders)

    def __next__(self):
        return next(self.item_orders)