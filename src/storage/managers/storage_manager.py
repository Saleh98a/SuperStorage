"""
Storage Manager class/interface
"""
from src.models.sector import Sector
from src.storage.storage_utils import insert_naive, insert_knapsack, extract_naive
from src.storage.storages.super_storage import SuperStorage
from src.models.forklift import SSForklift
from src.simulation.simulation_settings import InsertAlgorithm, ExtractAlgorithm


class StorageManager:
    def __init__(self, storage, insert_algo, extract_algo, sector_bounds=[]):
        self.storage = storage  # SuperStorage()
        self.forklift = SSForklift()
        self.insert_algorithm = insert_algo
        self.extract_algorithm = extract_algo
        self.sectors = []
        prev_bound = 0
        shelves_num = storage.storage_settings.shelves_num
        racks_per_row = storage.storage_settings.racks_per_row
        rows = storage.storage_settings.rows
        for bound in sector_bounds:
            current_sector = Sector.build_sector(prev_bound, bound-1, shelves_num, rows, racks_per_row)
            self.sectors.append(current_sector)
            prev_bound = bound

        last_sector = Sector.build_sector(prev_bound, rows+racks_per_row, shelves_num, rows, racks_per_row)
        self.sectors.append(last_sector)

    def insert_container(self, container):
        self.storage.move_forklift(self.forklift)  # Move forklift to (0,0,0)
        if self.insert_algorithm is InsertAlgorithm.NAIVE:  # TODO: maybe map is more elegant?
            insert_naive(self.storage, self.forklift, container)
        elif self.insert_algorithm is InsertAlgorithm.KNAPSACK:
            insert_knapsack(self.storage, self.forklift, container)
        else:
            raise Exception("Unknown Insertion Algorithm")

    def extract_order(self, order):
        if self.extract_algorithm is ExtractAlgorithm.NAIVE:
            extract_naive(self.storage, self.forklift, order)
        else:
            raise Exception("Unknown Extraction Algorithm")
        self.storage.move_forklift(self.forklift)  # Move forklift to (0,0,0)

    def get_fragmentation(self):
        return self.storage.get_fragmentation()

    def get_total_cost(self):
        return self.storage.total_cost

    def reset_storage(self):
        self.storage = SuperStorage(self.storage.storage_settings)
