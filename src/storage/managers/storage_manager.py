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

    def reset_storage(self):
        self.storage = SuperStorage(self.storage.storage_settings)

