"""
Storage Manager class/interface
"""
from src.events.event_bus import EventBus
from src.models.sector import Sector
from src.models.forklift import SSForklift
from src.storage.managers.storage_manager_settings import StorageManagerSettings
from src.storage.storage_utils import insert_naive, insert_knapsack, extract_naive, insert_optimized, extract_optimized
from src.storage.storages.super_storage import SuperStorage
from src.simulation.simulation_settings import InsertAlgorithm, ExtractAlgorithm


def build_sectors(sector_bounds, shelves_num, rows, racks_per_row):
    if not sector_bounds:
        sector = Sector.build_sector(0, rows + racks_per_row + 1, shelves_num, rows, racks_per_row)
        return [sector]
    sectors = [
        Sector.build_sector(0, sector_bounds[0] - 1, shelves_num, rows, racks_per_row),
        Sector.build_sector(sector_bounds[0], sector_bounds[1] - 1, shelves_num, rows, racks_per_row),
        Sector.build_sector(sector_bounds[1], sector_bounds[2] - 1, shelves_num, rows, racks_per_row),
        Sector.build_sector(sector_bounds[2], rows + racks_per_row + 1, shelves_num, rows, racks_per_row)
    ]
    return sectors


def most_frequent_percentage(products_info):
    total = 0
    products_num = len(products_info)
    top_level_percentage = [0.0 for _ in range(products_num)]
    for i in range(products_num):
        product_info = products_info[i]
        if product_info.frequency > 0.15:
            total += product_info.size_percentage
            top_level_percentage[i] = 1.0

    for i in range(products_num):
        # top_level_percentage[i] = 1.0 * top_level_percentage[i]
        top_level_percentage[i] = top_level_percentage[i] * products_info[i].size_percentage
        top_level_percentage[i] = top_level_percentage[i] / total
    return top_level_percentage


class StorageManager:
    def __init__(self, storage, settings=StorageManagerSettings(InsertAlgorithm.NAIVE, ExtractAlgorithm.NAIVE)):
        self.storage = storage
        self.forklift = SSForklift()
        self.settings = settings
        self.insert_algorithm = self.settings.insert_algorithm
        self.extract_algorithm = self.settings.extract_algorithm
        self.sectors = build_sectors(self.settings.sector_bounds,
                                     self.storage.storage_settings.shelves_per_rack,
                                     self.storage.storage_settings.rows,
                                     self.storage.storage_settings.racks_per_row)
        self.products_info = self.settings.learned_info
        self.top_level_percentage = most_frequent_percentage(self.products_info)
        if self.insert_algorithm == InsertAlgorithm.OPTIMIZED or self.extract_algorithm == ExtractAlgorithm.OPTIMIZED:
            for i in range(len(self.products_info)):
                if self.top_level_percentage[i] != 0:
                    print("product number", i, "top level frequency=", self.top_level_percentage[i])
        self.event_bus = EventBus()
        self.set_handlers()

    def insert_container(self, container):
        # TODO: Check if package size is bigger than shelf size
        # Note: this would impact runtime

        # Move forklift to (0,0,0)
        self.storage.move_forklift(self.forklift)

        if self.insert_algorithm is InsertAlgorithm.NAIVE:
            insert_naive(self.storage, self.forklift, container)
        elif self.insert_algorithm is InsertAlgorithm.KNAPSACK:
            insert_knapsack(self.storage, self.forklift, container)
        elif self.insert_algorithm is InsertAlgorithm.OPTIMIZED:
            insert_optimized(self, self.forklift, container)
        else:
            raise Exception("Unknown Insertion Algorithm")

    def extract_order(self, order):
        if self.extract_algorithm is ExtractAlgorithm.NAIVE:
            extract_naive(self.storage, self.forklift, order)
        elif self.extract_algorithm is ExtractAlgorithm.OPTIMIZED:
            extract_optimized(self, self.forklift, order)
        else:
            raise Exception("Unknown Extraction Algorithm")

        # Move forklift to (0,0,0)
        self.storage.move_forklift(self.forklift)

    def get_fragmentation(self):
        return self.storage.get_fragmentation()

    def get_total_cost(self):
        return self.storage.total_cost

    def get_insertion_cost(self):
        return self.storage.insertion_cost

    def get_extraction_cost(self):
        return self.storage.extraction_cost

    def reset_storage(self):
        self.storage = SuperStorage(self.storage.storage_settings, self.event_bus)

    def specifier(self):
        return str(self.insert_algorithm) + " " + str(self.extract_algorithm)

    def package_inserted_handler(self, package, position):
        for sector in self.sectors:
            if sector.has_position(position):
                sector.add_to_sector(package.product, package.quantity)

    def product_extracted_handler(self, product, quantity, position):
        for sector in self.sectors:
            if sector.has_position(position):
                sector.remove_from_sector(product, quantity)

    def set_handlers(self):
        self.event_bus.subscribe('package_inserted', self.package_inserted_handler)
        self.event_bus.subscribe('product_extracted', self.product_extracted_handler)

