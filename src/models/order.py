"""
Order model
Order is basically a list of ordered packages
"""
from src.models.product import Product


class Order:
    def __init__(self, product_orders=None):
        self.item_orders = product_orders
        if product_orders is None:
            self.item_orders = {}
        self.all_items_quantity = 0
        for item in self.item_orders:
            self.all_items_quantity += self.item_orders[item]

    # Returns quantity of product in order
    def get_product_quantity(self, item):
        return self.item_orders.get(item, 0)

    def add_to_order(self, product, quantity):
        if not isinstance(product, Product):
            raise Exception("incompatible arguments 1")
        self.item_orders[product] = self.item_orders.get(product, 0) + quantity
        self.all_items_quantity = self.all_items_quantity + quantity

    def remove_from_order(self, product, quantity):
        if not isinstance(product, Product):
            raise Exception("incompatible arguments 1")
        if quantity > self.get_product_quantity(product):
            raise Exception("Order doesn't need this much quantity")
        self.item_orders[product] = self.item_orders.get(product, 0) - quantity
        self.all_items_quantity = self.all_items_quantity - quantity

    def empty(self):
        return self.all_items_quantity == 0

    def __str__(self):
        ret = "Order: \n"
        for product in sorted(self.item_orders):
            ret += "    " + str(product) + "\n"
        return ret

    def __iter__(self):
        return iter(self.item_orders)

    def __next__(self):
        return next(self.item_orders)
