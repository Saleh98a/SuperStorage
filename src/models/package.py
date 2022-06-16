"""
Package model
Package is contains multiple products of the same type
"""

class Package:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def size(self):
        return self.quantity * self.product.size