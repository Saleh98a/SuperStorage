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


class ProductInfo:
    def __init__(self, frequency=0, size_percentage=0):
        self.frequency = frequency
        self.size_percentage = size_percentage
