"""
Our Storage Implementation
"""

from storage import Storage
from src.models.index import Rack, SSForklift, SSPosition
import math

class SuperStorage(Storage):

    def __int__(self, rows=20, racks_per_row=10, shelves_per_rack=10, weight_per_rack=math.inf, shelf_size=2):
        super().__init__()
        self.rows = rows
        self.racks_per_row = racks_per_row
        self.num_of_racks = rows * racks_per_row
        self.shelves_per_rack = shelves_per_rack
        self.weight_per_rack = weight_per_rack
        self.rack_size = shelf_size
        self.racks = [[Rack(shelves_per_rack, shelf_size) for _ in range(racks_per_row)] for _ in range(rows)]
        # additional info
        self.items_map = {}

    def insert_package(self, forklift, package, position=None):
        self.move_forklift(forklift, position)
        self.racks[position.row][position.col].shelves[position.shelf_num].put_package(package)
        # save/update additional info
        self.items_map[package.name] = self.items_map.get(package.name, []).append(position)

    def extract_item(self, forklift, item, quantity, position=None):
        self.move_forklift(forklift, position)
        new_quantity = self.racks[position.row][position.col].shelves[position.shelf_num].extract_order(item, quantity)
        # save/update additional info
        if new_quantity == 0:
            self.items_map[item] = self.items_map[item].remove(position)

    def calculate_forklift_cost(self, forklift, position):
        if forklift.position.row == position.row:
            return abs(forklift.position.col - position.col)
        return abs(forklift.position.row - position.row) + min(forklift.position.col + position.col, 2 * self.racks_per_row - forklift.position.col - position.col)

    def move_forklift(self, forklift, position):
        # Check if forklift is SSForklift and position is SSPosition
        if not isinstance(forklift, SSForklift) or not isinstance(position, SSPosition):
            raise Exception("incompatible arguments")
        forklift.position = position

    def get_items_at(self, position):
        return self.racks[position.row][position.col].shelves[position.shelf_num].item_quantities

    def get_item_quantity_at(self, item, position):
        item_quantities = self.racks[position.row][position.col].shelves[position.shelf_num].item_quantities
        return item_quantities.get(item, 0)

    def can_put_package_at(self, container, position):
        return self.racks[position.row][position.col].shelves[position.shelf_num].can_put_package(container)

    def __iter__(self):
        self.iter_pos = SSPosition(0, 0, 0)
        return self

    def __next__(self):
        self.iter_pos = SSPosition(self.iter_pos.row, self.iter_pos.col, self.iter_pos.shelf_num)
        if self.iter_pos.col < self.racks_per_row:
            self.iter_pos.col = self.iter_pos.col + 1
        else:
            self.iter_pos.col = 0
            self.iter_pos.row = self.iter_pos.row + 1

        if self.iter_pos.row == self.rows:
            return None

        return self.iter_pos
