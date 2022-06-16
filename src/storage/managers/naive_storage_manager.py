"""
Naive Storage Manager implementation
"""
from src.storage.managers.storage_manager import StorageManager
from src.storage.storage_utils import insert_naive, extract_naive
from src.models.forklift import SSForklift


class NaiveStorageManager(StorageManager):

    def __init__(self, storage):
        super().__init__(storage)
        self.forklift = SSForklift()

    def insert_container(self, container):
        insert_naive(self.storage, self.forklift, container)

    def extract_order(self, order):
        extract_naive(self.storage, self.forklift, order)

    def print(self):
        self.storage.print()
