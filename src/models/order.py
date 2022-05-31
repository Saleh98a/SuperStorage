"""
Order model
Order is basically a list of orderer packages
"""

class Order:
    def __init__(self, item_orders={}):
        self.item_orders = item_orders

    def add_order(self, order):
        self.item_orders.add(order)

    def remove_order(self, order):
        self.item_orders.remove(order)