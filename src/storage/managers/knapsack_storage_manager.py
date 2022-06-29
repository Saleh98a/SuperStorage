from src.storage.managers.storage_manager import StorageManager
from src.storage.storage_utils import insert_knapsack, extract_naive
from src.models.forklift import SSForklift


class KnapsackStorageManager(StorageManager):

    def __init__(self, storage):
        super().__init__(storage)
        self.forklift = SSForklift()

    def insert_container(self, container):
        self.storage.move_forklift(self.forklift)
        insert_knapsack(self.storage, self.forklift, container)

    def extract_order(self, order):
        extract_naive(self.storage, self.forklift, order)

    def print(self):
        self.storage.print()
