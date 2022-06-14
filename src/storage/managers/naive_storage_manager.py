"""
Naive Storage Manager implementation
"""
from storage_manager import StorageManager
from src.storage.storage_utils import insert_naive

class NaiveStorageManager(StorageManager):

    def __init__(self, storage):
        super().__init__(storage)

    def insert_container(self, container):
        insert_naive(self.storage, container)

    def extract_order(self, order):
        pass