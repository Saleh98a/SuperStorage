"""
Storage Manager class/interface
"""

from abc import ABC, abstractmethod

from src.storage.storages.super_storage import SuperStorage


class StorageManager(ABC):

    def __init__(self, storage):
        self.storage = storage

    @abstractmethod
    def insert_container(self, container):
        pass

    @abstractmethod
    def extract_order(self, order):
        pass

    def get_fragmentation(self):
        return self.storage.get_fragmentation()

    def get_total_cost(self):
        return self.storage.total_cost

    def reset_storage(self, rows=20, racks_per_row=10, shelves_per_rack=10, shelf_size=200):
        self.storage = SuperStorage(rows, racks_per_row, shelves_per_rack, shelf_size)

