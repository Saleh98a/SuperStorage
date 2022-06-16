"""
Our Storage Implementation
"""

from src.storage.storages.storage import Storage
# from src.models.index import Rack, SSForklift, SSPosition
from src.models.rack import Rack
from src.models.forklift import SSForklift
from src.models.position import SSPosition
import math


class SuperStorage(Storage):
    def __init__(self, rows=20, racks_per_row=10, shelves_per_rack=10, weight_per_rack=math.inf, shelf_size=20):
        super().__init__()
        self.rows = rows
        self.racks_per_row = racks_per_row
        self.num_of_racks = rows * racks_per_row
        self.shelves_per_rack = shelves_per_rack
        self.weight_per_rack = weight_per_rack
        self.rack_size = shelf_size
        self.racks = [[Rack(shelves_per_rack, shelf_size) for _ in range(racks_per_row)] for _ in range(rows)]  # todo simplify
        # for e in self.racks:
        #     print("rack")
        #     for p in e:
        #         print("shelf")
        # # additional info
        self.items_map = {}

    def get_shelf(self, position):
        return self.racks[position.row][position.col].shelves[position.shelf_num]

    def insert_package(self, forklift, package, position=None):
        self.move_forklift(forklift, position)
        self.racks[position.row][position.col].shelves[position.shelf_num].put_package(package)
        # save/update additional info
        #print("printing absr sho", self.items_map)
        #self.items_map[package.product.name] = self.items_map.get(package.product.name, default=[]).append(position)
        if package.product not in self.items_map:
            self.items_map[package.product] = []
        self.items_map[package.product].append(position)
        #print("printing absr sho", self.items_map)

    def extract_product(self, forklift, product, quantity, position=None):
        self.move_forklift(forklift, position)
        new_quantity = self.racks[position.row][position.col].shelves[position.shelf_num].extract_order(product, quantity)
        # save/update additional info
        if new_quantity == 0:
            print("No more quantity of ", product)
            print("Kaiyal: ", self.items_map[product])
            print("r row: ", position.row)
            print("r col: ", position.col)
            print("r shelf_num: ", position.shelf_num)
            for pos in self.items_map[product]:
                print("row: ", pos.row)
                print("col: ", pos.col)
                print("shelf_num: ", pos.shelf_num)
            self.items_map[product].remove(position)

    def calculate_forklift_cost(self, forklift, position):
        if forklift.position.row == position.row:
            return abs(forklift.position.col - position.col)
        return abs(forklift.position.row - position.row) + min(forklift.position.col + position.col,
                                                               2 * self.racks_per_row - forklift.position.col - position.col)

    def move_forklift(self, forklift, position):
        # Check if forklift is SSForklift and position is SSPosition
        if not isinstance(forklift, SSForklift):
            raise Exception("incompatible arguments 1")
        if not isinstance(position, SSPosition):
            raise Exception("incompatible arguments 2")
        forklift.position = position

    def get_items_at(self, position):
        return self.racks[position.row][position.col].shelves[position.shelf_num].item_quantities

    def get_item_quantity_at(self, item, position):
        item_quantities = self.racks[position.row][position.col].shelves[position.shelf_num].item_quantities
        return item_quantities.get(item, 0)

    def can_put_package_at(self, package, position):
        # print("Pos row = " + str(position.row))
        #       print("Pos col = " + str(position.col))
        return self.racks[position.row][position.col].shelves[position.shelf_num].can_put_package(package)

    def __iter__(self):
        self.iter_pos = SSPosition(0, 0, 0)
        return self

    def __next__(self):
        temp = SSPosition(self.iter_pos.row, self.iter_pos.col, self.iter_pos.shelf_num)
        if self.iter_pos.shelf_num + 1 < self.shelves_per_rack:
            self.iter_pos.shelf_num += 1
        elif self.iter_pos.col + 1 < self.racks_per_row:
            self.iter_pos.shelf_num = 0
            self.iter_pos.col += 1
        else:
            self.iter_pos.shelf_num = 0
            self.iter_pos.col = 0
            self.iter_pos.row += 1

        if temp.row == self.rows:
            raise StopIteration

        return temp

    def print(self):
        for position in self:
            print("shelf num", position.shelf_num)
            if position.shelf_num == 0:
                if position.col == 0:
                    # New Rack in New Column
                    if position.row != 0 :
                        print("")
                        print("")
                        print("")
                        print("")
                else:
                    # New Rack
                    print("___________________________")
            curr_shelf = self.get_shelf(position)
            curr_shelf.print()
