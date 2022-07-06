"""
Our Storage Implementation
"""

from src.storage.storages.storage import Storage
from src.storage.storages.storage_settings import StorageSettings
# from src.models.index import Rack, SSForklift, SSPosition
from src.models.rack import Rack
from src.models.forklift import SSForklift
from src.models.position import SSPosition


class SuperStorage(Storage):
    def __init__(self, storage_settings=StorageSettings()):
        super().__init__()
        self.storage_settings = storage_settings

        rows = storage_settings.rows
        racks_per_row = storage_settings.racks_per_row
        shelves_per_rack = storage_settings.shelves_per_rack
        shelf_size = storage_settings.shelf_size

        self.rack_size = shelf_size * shelves_per_rack
        self.num_of_racks = storage_settings.rows * storage_settings.racks_per_row
        self.racks = [[Rack(shelves_per_rack, shelf_size) for _ in range(racks_per_row)] for _ in range(rows)]
        # additional info
        self.items_map = {}
        self.total_cost = 0

    def get_shelf(self, position):
        return self.racks[position.row][position.col].shelves[position.shelf_num]

    def insert_package(self, forklift, package, position=None):
        self.move_forklift(forklift, position)
        self.racks[position.row][position.col].shelves[position.shelf_num].put_package(package)

        # save/update additional info
        # self.items_map[package.product.name] = self.items_map.get(package.product.name, default=[]).append(position)
        self.racks[position.row][position.col].used_size += package.size()

        if package.product not in self.items_map:
            self.items_map[package.product] = []
        self.items_map[package.product].append(position)

    def extract_product(self, forklift, product, quantity, position=None):
        self.move_forklift(forklift, position)
        # current_quantity = self.racks[position.row][position.col].shelves[position.shelf_num].get_quantity(product)
        # if current_quantity == 0:
        #     return current_quantity
        # max_quant = min(quantity, current_quantity)
        extracted_quantity = self.racks[position.row][position.col].shelves[position.shelf_num].extract_order(product,
                                                                                                              quantity)
        # save/update additional info
        self.racks[position.row][position.col].used_size -= extracted_quantity * product.size

        if extracted_quantity <= quantity and not extracted_quantity == 0:
            for position_to_check in self.items_map[product]:
                if position_to_check.row == position.row and position_to_check.col == position.col:
                    if position_to_check.shelf_num == position.shelf_num:
                        self.items_map[product].remove(position_to_check)
                        break
        return extracted_quantity

    def calculate_forklift_cost(self, forklift, position):
        # do not forget to multiply with the horizontal\vertical coef
        if forklift.position.row == position.row:
            return abs(forklift.position.col - position.col) + abs(position.shelf_num - forklift.position.shelf_num)
        return abs(forklift.position.row - position.row) + \
               abs(position.shelf_num - forklift.position.shelf_num) + \
               min(forklift.position.col + position.col,
                   2 * self.storage_settings.racks_per_row - forklift.position.col - position.col)

    def move_forklift(self, forklift, position=SSPosition(0, 0, 0)):
        # Check if forklift is SSForklift and position is SSPosition
        if not isinstance(forklift, SSForklift):
            raise Exception("incompatible arguments 1")
        if not isinstance(position, SSPosition):
            raise Exception("incompatible arguments 2")
        self.total_cost += self.calculate_forklift_cost(forklift, position)
        forklift.position = position

    def get_items_at(self, position):
        return self.racks[position.row][position.col].shelves[position.shelf_num].item_quantities

    def get_item_quantity_at(self, item, position):
        item_quantities = self.racks[position.row][position.col].shelves[position.shelf_num].item_quantities
        return item_quantities.get(item, 0)

    def can_put_package_at(self, package, position):
        return self.racks[position.row][position.col].shelves[position.shelf_num].can_put_package(package)

    def get_fragmentation(self):
        maximum_shelf = 0
        i = 0
        wasted_space = 0
        for row in range(self.storage_settings.rows):
            for col in range(self.storage_settings.racks_per_row):
                for shelf in self.racks[row][col].shelves:
                    i += 1
                    if shelf.is_used():
                        maximum_shelf = i
                        wasted_space += (shelf.size - shelf.used_size)*100/shelf.size
        return wasted_space/maximum_shelf

    def __iter__(self):
        self.iter_pos = SSPosition(0, 0, 0)
        return self

    def __next__(self):
        temp = SSPosition(self.iter_pos.row, self.iter_pos.col, self.iter_pos.shelf_num)
        if self.iter_pos.shelf_num + 1 < self.storage_settings.shelves_per_rack:
            self.iter_pos.shelf_num += 1
        elif self.iter_pos.col + 1 < self.storage_settings.racks_per_row:
            self.iter_pos.shelf_num = 0
            self.iter_pos.col += 1
        else:
            # TODO change so that we continue from col and just change row
            self.iter_pos.shelf_num = 0
            self.iter_pos.col = 0
            self.iter_pos.row += 1

        if temp.row == self.storage_settings.rows:
            raise StopIteration

        return temp

    def print(self):
        for position in self:
            if position.shelf_num == 0:
                if position.col == 0:
                    # New Rack in New Column
                    if position.row != 0:
                        print("")
                        print("")
                        print("")
                        print("")
                else:
                    # New Rack
                    print("___________________________")
            curr_shelf = self.get_shelf(position)
            curr_shelf.print()
