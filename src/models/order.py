"""
Order model
Order is basically a list of ordered packages
"""

class Order:
    def __init__(self, product_orders={}):
        self.item_orders = product_orders
        self.all_items_quantity = 0
        for item in product_orders:
            self.all_items_quantity += product_orders[item]

    def get_order(self, item):
        return self.item_orders.get(item, 0)

    def add_to_order(self, item, quantity):
        self.item_orders[item] = self.item_orders.get(item, 0) + quantity
        self.all_items_quantity = self.all_items_quantity + quantity

    def remove_from_order(self, item, quantity):
        if quantity > self.get_order(item):
            raise Exception("Order doesn't need this much quantity")
        self.item_orders[item] = self.item_orders.get(item, 0) - quantity
        self.all_items_quantity = self.all_items_quantity - quantity

    def empty(self):
        return self.all_items_quantity == 0

    def __iter__(self):
        return iter(self.item_orders)

    def __next__(self):
        return next(self.item_orders)
