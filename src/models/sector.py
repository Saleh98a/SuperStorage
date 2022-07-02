"""
Territory Info Class
"""

from src.models.index import SSPosition

class Sector:
    def __init__(self, positions, pos_size=200):
        self.positions = positions
        self.total_size = positions.size() * pos_size
        self.item_quantities = {}

    def get_quantity(self, item):
        return self.item_quantities.get(item, 0)

    def get_percentage(self, item):
        return (self.get_quantity(item) * item.size * 1.0) / self.total_size

    def add_to_sector(self, item, quantity):
        self.item_quantities[item] = self.item_quantities.get(item, 0) + quantity

    def remove_from_sector(self, item, quantity):
        if quantity > self.get_quantity(item):
            raise Exception("Sector didn't have this much quantity")
        self.item_quantities[item] = self.item_quantities.get(item, 0) - quantity

    # returns positions that comply with: pos.row in rows && pos.col in cols && pos.shelf in shelves
    @staticmethod
    def build_sector(rows, racks, shelves):
        positions = []
        for row in rows:
            for rack in racks:
                for shelf in shelves:
                    positions.append(SSPosition(row, rack, shelf))
        return Sector(positions)