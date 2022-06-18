"""
Shelf model
Shelf has a size and can hold a number of packages
"""

import math


class Shelf:
    def __init__(self, size, weight_limit=math.inf):
        self.size = size
        self.used_size = 0
        self.item_quantities = {}

    def put_package(self, package):
        if not self.can_put_package(package):
            raise Exception("Package can't fit on this shelf")
        self.used_size += package.size()
        self.item_quantities[package.product] = self.item_quantities.get(package.product, 0) + package.quantity

    def extract_order(self, item, quantity): # we return the quantity that we extracted from this shelf
        if quantity == 0:
            return 0
        if quantity < 0:
            raise Exception("Invalid order quantity")
        current_quantity = self.item_quantities.get(item, 0)
        if current_quantity == 0:
            return 0
        if current_quantity > quantity:
            self.item_quantities[item] = current_quantity - quantity
        else:
            self.item_quantities.pop(item)
        return min(current_quantity,quantity)

    def can_put_package(self, package):
        return (package.size() + self.used_size) <= self.size

    def print(self):
        if self.used_size == 0:
            return
        print("Using " + str(self.used_size) + " out of " + str(self.size) + " size units, Packages:", end="\t")
        for product in self.item_quantities:
            print(product.name, "of size", product.size, "quantity", self.item_quantities[product], end=", ")
        print("")
