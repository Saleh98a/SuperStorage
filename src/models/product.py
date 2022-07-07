"""
Product model
"""


class Product:
    def __init__(self, id, name, weight, size, category):
        self.id = id
        self.name = name
        self.weight = weight
        self.size = size
        # TODO: check if needed and create a type if so
        self.category = category

    def __hash__(self) -> int:
        return self.name.__hash__()

    def __str__(self) -> str:
        return "Product ID: " + str(self.id) + " Name: " + str(self.name) + " Size: " + str(self.size)

    def __lt__(self, other):
        return self.id < other.id


class ProductInfo:
    def __init__(self, frequency=0, size_percentage=0):
        self.frequency = frequency
        self.size_percentage = size_percentage
