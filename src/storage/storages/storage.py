"""
Storage class/interface
"""

from abc import ABC, abstractmethod


class StorageSettings:
    def __init__(self, rows=20, racks_per_row=20, shelves_per_rack=10, shelf_size=200):
        self.rows = rows
        self.racks_per_row = racks_per_row
        self.shelves_per_rack = shelves_per_rack
        self.shelf_size = shelf_size


class Storage(ABC):

    @abstractmethod
    def insert_package(self, forklift, package, position):
        pass

    @abstractmethod
    def extract_product(self, forklift, product, quantity, position):
        pass

    @abstractmethod
    def calculate_forklift_cost(self, forklift, position):
        pass

    @abstractmethod
    def move_forklift(self, forklift, position):
        pass

    @abstractmethod
    def get_items_at(self, position):
        pass

    @abstractmethod
    def get_item_quantity_at(self, item, position):
        pass

    @abstractmethod
    def can_put_package_at(self, package, position):
        pass

    @abstractmethod
    def get_fragmentation(self):
        pass

    @abstractmethod
    def print(self):
        pass
