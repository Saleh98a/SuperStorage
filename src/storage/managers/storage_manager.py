"""
Storage Manager class/interface
"""
from random import randint

import numpy as np

from src.models.product import ProductInfo
from src.models.sector import Sector
from src.storage.storage_utils import insert_naive, insert_knapsack, extract_naive, insert_optimized, extract_optimized
from src.storage.storages.super_storage import SuperStorage
from src.models.forklift import SSForklift
from src.simulation.simulation_settings import InsertAlgorithm, ExtractAlgorithm


def build_sectors(sector_bounds, shelves_num, rows, racks_per_row):
    if not sector_bounds:
        return sector_bounds
    first_sector = Sector.build_sector(0, sector_bounds[0]-1, shelves_num, rows, racks_per_row)
    second_sector = Sector.build_sector(sector_bounds[0], sector_bounds[1]-1, shelves_num, rows, racks_per_row)
    third_sector = Sector.build_sector(sector_bounds[1], sector_bounds[2]-1, shelves_num, rows, racks_per_row)
    last_sector = Sector.build_sector(sector_bounds[2], rows + racks_per_row + 1, shelves_num, rows, racks_per_row)
    sectors = [first_sector, second_sector, third_sector, last_sector]
    return sectors


def most_frequent_percentage(products_info):
    total = 0
    products_num = len(products_info)
    top_level_percentage = [0 for _ in range(products_num)]
    for i in range(products_num):
        product_info = products_info[i]
        if product_info.frequency > 0.1:
            total += product_info.size_percentage
            top_level_percentage[i] = 1

    for i in range(products_num):
        top_level_percentage[i] = 1.0 * top_level_percentage[i]
        top_level_percentage[i] = top_level_percentage[i] * products_info[i].size_percentage
        top_level_percentage[i] = top_level_percentage[i] / total
    return top_level_percentage


def learn(products, sample_size):
    print("starting to learn our distribution :-")
    # size[i]/total_size
    # product_quantity_mean/all_quantities (This isn't what we want)
    # => size[i]*product_quantity_mean / sigma_quantity (size[j])
    # Each product quantity is poisson distribution with quantities_lambda[i] parameter for product i
    products_num = len(products)
    quantities_lambda = [randint(1, 5) for _ in
                         range(products_num)]  # the lambda of every product quantity distribution
    # mu and sigma are the parameters for normal distribution
    scale = randint(30, 80)
    # sample of products num that distributed with normal distribution  with sigma and mu parameters
    # possible_orders_product = np.random.normal(mu, sigma, sample_size)
    possible_orders_product = np.random.exponential(scale, sample_size) #[randint(0, products_num - 1) for _ in range(sample_size)]
    total_products_size = []
    total_size = 0
    total_products_size = [0 for i in range(products_num)]
    total_products_orders = [0 for i in range(products_num)]
    order_num = 0
    order_len = randint(1, 50)
    current_len = 0
    current_order_products = [False for i in range(products_num)]
    for i in range(sample_size):
        if current_len == order_len or i == sample_size-1:
            current_order_products = [False for i in range(products_num)]
            order_num += 1
            order_len = randint(1, 50)
            current_len = 0
        current_len += 1

        while possible_orders_product[i] < 0 or possible_orders_product[i] > products_num:
            possible_orders_product[i] = np.random.exponential(scale, 1)[0]
        possible_orders_product[i] = int(possible_orders_product[i])
        lamda = quantities_lambda[int(possible_orders_product[i])]
        quantity = int(np.random.poisson(lamda, 1)[0])
        #total_products_size.append(int(quantity * products[possible_orders_product[i]].size))
        if current_order_products[int(possible_orders_product[i])]:
            total_products_orders[int(possible_orders_product[i])] += 1
        else:
            current_order_products[int(possible_orders_product[i])] = True
        total_products_size[int(possible_orders_product[i])] += int(quantity * products[int(possible_orders_product[i])].size)
        total_size += int(quantity * products[int(possible_orders_product[i])].size)

    # to save for each product percentage of orders he appears on it and percentage of his size from total size
    products_info = []
    for i in range(products_num):
        frequency = total_products_orders[i]/order_num
        size_percentage = total_products_size[i]/total_size
        current_info = ProductInfo(frequency, size_percentage)
        products_info.append(current_info)
    return products_info


class StorageManager:
    def __init__(self, storage, insert_algo, extract_algo, sector_bounds=[], learned_info=[]):
        self.storage = storage  # SuperStorage()
        self.forklift = SSForklift()
        self.insert_algorithm = insert_algo
        self.extract_algorithm = extract_algo
        shelves_num = storage.storage_settings.shelves_per_rack
        rows = storage.storage_settings.rows
        racks_per_row = storage.storage_settings.racks_per_row
        self.sectors = build_sectors(sector_bounds, shelves_num, rows, racks_per_row)
        self.products_info = learned_info
        self.top_level_percentage = most_frequent_percentage(learned_info)
        for i in range(len(learned_info)):
            print("product number", i, "top level frequency=", self.top_level_percentage[i])

    def insert_container(self, container):
        self.storage.move_forklift(self.forklift)  # Move forklift to (0,0,0)
        if self.insert_algorithm is InsertAlgorithm.NAIVE:  # TODO: maybe map is more elegant?
            insert_naive(self.storage, self.forklift, container)
        elif self.insert_algorithm is InsertAlgorithm.KNAPSACK:
            insert_knapsack(self.storage, self.forklift, container)
        else:
            insert_optimized(self, self.forklift, container)

    def extract_order(self, order):
        if self.extract_algorithm is ExtractAlgorithm.NAIVE:
            extract_naive(self.storage, self.forklift, order)
        else:
            extract_optimized(self, self.forklift, order)
        self.storage.move_forklift(self.forklift)  # Move forklift to (0,0,0)

    def get_fragmentation(self):
        return self.storage.get_fragmentation()

    def get_total_cost(self):
        return self.storage.total_cost

    def reset_storage(self):
        self.storage = SuperStorage(self.storage.storage_settings)
