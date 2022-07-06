"""
Territory Info Class
"""

from src.models.index import SSPosition


class Sector:
    def __init__(self, positions, pos_size=200):
        self.positions = positions
        self.total_size = len(positions) * pos_size
        self.item_quantities = {}

    def get_quantity(self, item):
        if item in self.item_quantities.keys():
            return self.item_quantities.get(item)
        return 0

    def get_percentage(self, item):
        return (self.get_quantity(item) * item.size * 1.0) / self.total_size

    def add_to_sector(self, item, quantity):
        if self.get_quantity(item):
            self.item_quantities[item] += quantity
        else:
            self.item_quantities[item] = quantity

    def remove_from_sector(self, item, quantity):
        if quantity <= 0:
            raise Exception("invalid quantity")

        if quantity > self.get_quantity(item):
            raise Exception("Sector didn't have this much quantity", self.total_size)

        self.item_quantities[item] -= quantity
        if self.item_quantities[item] == 0:
            self.item_quantities.pop(item)

    @staticmethod
    def check_if_in_range(row, col, min_dist, max_dist):
        if row + col > max_dist:
            return False
        if row + col < min_dist:
            return False
        return True

    # returns positions that comply with: pos.row in rows && pos.col in cols && pos.shelf in shelves
    @staticmethod
    def build_sector(min_dist, max_dist, shelves_num, storage_rows, storage_racks_per_row):
        positions = []
        for i in range(max_dist + 1):
            for j in range(max_dist + 1):
                for k in range(shelves_num):
                    distance = i+j
                    if min_dist <= distance <= max_dist:
                        if i < storage_rows and j < storage_racks_per_row:
                            position = SSPosition(i, j, k)
                            positions.append(position)
        return Sector(positions)
