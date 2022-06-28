"""
Storage Manager class/interface
"""

from abc import ABC, abstractmethod


class StorageManager(ABC):

    def __init__(self, storage):
        self.storage = storage

    @abstractmethod
    def insert_container(self, container):
        pass

    @abstractmethod
    def extract_order(self, order):
        pass

    def get_space(self):
        return self.storage.get_fragmentation()
