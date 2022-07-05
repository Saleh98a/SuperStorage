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
            self.item_quantities[item] = self.item_quantities.get(item, 0) + quantity
        else:
            self.item_quantities[item] = quantity

    def remove_from_sector(self, item, quantity):
        if quantity <= 0:
            raise Exception("invalid quantity")

        if quantity > self.get_quantity(item):
            raise Exception("Sector didn't have this much quantity")

        self.item_quantities[item] -= quantity
        if self.item_quantities[item] == 0:
            self.item_quantities.pop(item)

    def __iter__(self):
        self.current_pos = 0
        return self.positions[self.current_pos]

    def __next__(self):
        if self.current_pos == len(self.positions):
            raise StopIteration
        temp = self.positions[self.current_pos]
        self.current_pos += 1
        return temp


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
        for k in range(max_dist + 1):
            for j in range(k + 1):
                i = k - j
                if i < storage_rows and j < storage_racks_per_row:
                    if Sector.check_if_in_range(i, j, min_dist, max_dist):
                        for shelf_num in range(shelves_num):
                            positions.append(SSPosition(i, j, shelf_num))
        return Sector(positions)
