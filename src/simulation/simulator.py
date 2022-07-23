"""
Simulator Class
Runs a storage environment simulation
"""
import math
import random
from random import randint
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from src.models.container import Container
from src.models.order import Order
from src.models.package import Package
from src.models.product import Product, ProductInfo

from src.storage.managers.storage_manager import StorageManager
from src.storage.storages.super_storage import SuperStorage
from src.simulation.simulation_settings import SimulationSettings

from copy import copy
from src.simulation.io_utils import *

def initialize_containers(products, containers_num, packages_num_per_container, shelf_size):
    containers = []
    for container in range(containers_num):
        packages = []
        for package in range(packages_num_per_container):
            product = products[randint(0, 99)]
            quantity = randint(1, shelf_size // product.size)
            p = Package(product, quantity)
            packages.append(p)
        containers.append(Container(packages))
    return containers


def get_exponential_list(exponential_lambda, products_num, size):
    product_id_list = np.random.exponential(exponential_lambda, size)
    for i in range(size):
        while product_id_list[i] < 0 or product_id_list[i] >= products_num:
            product_id_list[i] = int(np.random.exponential(exponential_lambda))
    return product_id_list.astype(int)


def draw_order(products, lambda_val=3, products_per_order=10):
    """
    Distributions:
        - Each product quantity: Poisson Distribution
            Parameter: Lambda = quantities_lambda[i] (Chosen randomly from 1-5 incl.)

        - Picking the product: Exponential Distribution (not critical)
            Parameter: Lambda = exponential_lambda (Chosen randomly from 30-80 incl.)


    """
    quantity_lambda_list = [lambda_val for _ in range(len(products))]  # TODO revert this to randint(1,5)
    exponential_lambda = 40  # TODO revert this to randint(30,80)
    order_len = np.random.randint(products_per_order//2, products_per_order)

    # print("Printing order len list")
    # for i in range(len(order_len_list)):
    #     print(order_len_list[i])

    # print("order len list sum", order_len_list.sum())
    product_id_list = get_exponential_list(exponential_lambda, len(products), order_len)

    idx = 0
    order = Order()
    for _ in range(order_len):
        prod_id = product_id_list[idx]
        quantity_lambda = quantity_lambda_list[prod_id]
        quantity = int(np.random.poisson(quantity_lambda))
        # print("Addition of id", prod_id, "Quantity", quantity)
        order.add_to_order(products[prod_id], quantity)
        idx += 1

    return order

def draw_orders(products, orders_count):
    return [draw_order(products) for _ in range(orders_count)]



def draw_container(products, package_max_size, lambda_val=3, packages_per_container=60):
    """
    Distributions:
        - Each product quantity: Poisson Distribution
            Parameter: Lambda = quantities_lambda[i] (Chosen randomly from 1-5 incl.)

        - Picking the product: Exponential Distribution (not critical)
            Parameter: Lambda = exponential_lambda (Chosen randomly from 30-80 incl.)


    """
    quantity_lambda_list = [lambda_val for _ in range(len(products))]  # TODO revert this to randint(...)
    exponential_lambda = 40  # TODO revert this to randint(30,80)
    container_len = np.random.randint(packages_per_container//2, packages_per_container)

    product_id_list = get_exponential_list(exponential_lambda, len(products), container_len)

    idx = 0
    container = Container()
    for _ in range(container_len):
        prod_id = product_id_list[idx]
        quantity_lambda = quantity_lambda_list[prod_id]
        quantity = int(np.random.poisson(quantity_lambda))
        product = products[prod_id]
        max_quantity_per_package = package_max_size // product.size
        num_of_packages = math.ceil(quantity / max_quantity_per_package)
        for _ in range(num_of_packages):
            quantity_in_package = min(max_quantity_per_package, quantity)
            container.add_package(Package(products[prod_id], quantity_in_package))
            quantity -= quantity_in_package
        idx += 1

    return container

def draw_containers(products, containers_count, package_max_size):
    return [draw_container(products, package_max_size) for _ in range(containers_count)]


def learn(products, total_orders):
    print("---------------Learning---------------")
    products_num = len(products)

    orders = draw_orders(products, total_orders)

    # Get total size & total orders of each product
    total_size = 0
    total_size_of_product = [0 for _ in range(products_num + 1)]
    total_orders_of_product = [0 for _ in range(products_num + 1)]
    for order in orders:
        current_order_products = [False for _ in range(products_num + 1)]
        for product in order.item_orders:
            if not current_order_products[product.id]:
                total_orders_of_product[product.id] += 1
            current_order_products[product.id] = True
            total_size_of_product[product.id] += order.get_product_quantity(product) * product.size
            total_size += order.get_product_quantity(product) * product.size

    # Calculate frequency & size percentage of each product
    products_info = []
    for i in range(products_num):
        frequency = total_orders_of_product[i] / total_orders
        size_percentage = total_size_of_product[i] / total_size
        current_info = ProductInfo(frequency, size_percentage)
        products_info.append(current_info)
    print("---------------Done learning---------------")
    return products_info


def fix_order(storage, order):
    fixed_order = Order()
    for product in order.item_orders:
        quantity = min(order.item_orders[product], storage.get_item_quantity(product))
        if quantity > 0:
            fixed_order.add_to_order(product, quantity)
    return fixed_order


class Simulator:
    def __init__(self, simulation_settings=SimulationSettings()):
        self.simulation_settings = simulation_settings
        self.operations_num = self.simulation_settings.operations_num
        self.repetitions_num = self.simulation_settings.repetitions_num
        self.extraction_probability = self.simulation_settings.extraction_probability
        self.insertion_headstart = self.simulation_settings.insertion_headstart
        self.curr_fragmentation = 0
        self.curr_cost = 0
        self.curr_runtime = 0

        self.products = initialize_products()

        self.learned_info = learn(self.products, 500)

        self.storage_managers = []
        self.graphs = {
            'Fragmentation': {},
            'Cost': {},
            'Insertion Cost': {},
            'Extraction Cost': {},
        }
        for storage_manager_settings in self.simulation_settings.storage_managers_settings:
            storage_manager_settings.learned_info = self.learned_info
            storage_manager = StorageManager(SuperStorage(self.simulation_settings.storage_settings),
                                             storage_manager_settings)
            self.storage_managers.append(storage_manager)
            for graph in self.graphs:
                self.graphs[graph][storage_manager.specifier()] = [0 for _ in range(0, self.operations_num)]

        plt.ion()

    def print_plots(self, repetition):
        fig = plt.figure()
        axs = []
        i = 1
        for graph_name in self.graphs:

            x_values = list(range(1, self.operations_num + 1))

            # plotting the points
            for manager in self.graphs[graph_name]:
                y_values = [y / repetition for y in self.graphs[graph_name][manager]]
                plt.plot(x_values, y_values, label=manager)

            # naming the x axis
            plt.xlabel('steps')
            # naming the y axis
            self.ylabel = plt.ylabel(graph_name)

            # giving a title to my graph
            plt.title(graph_name)

            # function to show the plot
            plt.legend()
            plt.show(block=False)

    def reset_costs(self):
        self.curr_fragmentation = 0
        self.curr_cost = 0
        self.curr_runtime = 0

    def simulate(self):
        # Print data
        print(self)

        for repetition in range(self.repetitions_num):  # need to get from simulation settings
            for storage_manager in self.storage_managers:
                storage_manager.reset_storage()
            self.reset_costs()

            for curr_operation in tqdm(range(0, self.operations_num)):
                # Choose next step
                is_extract = curr_operation >= self.insertion_headstart and random.random() <= self.extraction_probability
                if not is_extract:
                    chosen_container = draw_container(products=self.products,
                                                      package_max_size=self.simulation_settings.storage_settings.shelf_size,
                                                      # lambda_val=(3 * (self.extraction_probability) / (1 - self.extraction_probability)),
                                                      lambda_val=(100),
                                                      packages_per_container=self.simulation_settings.packages_per_container)
                else:
                    chosen_order = draw_order(products=self.products,
                                              # lambda_val=(1 * (1 - self.extraction_probability) / (self.extraction_probability)),
                                              lambda_val=(10),
                                              products_per_order=self.simulation_settings.products_per_order)
                    order = fix_order(self.storage_managers[0].storage, chosen_order)

                for storage_manager in self.storage_managers:
                    # print("op {0} sm {1}", curr_operation, storage_manager)
                    # Insert the container
                    if not is_extract:
                        storage_manager.insert_container(chosen_container)
                    else:
                        order_copy = copy(order)
                        order_copy.item_orders = copy(order.item_orders)
                        storage_manager.extract_order(order_copy)

                    # Update Costs
                    curr_fragmentation = storage_manager.get_fragmentation()
                    curr_cost = storage_manager.get_total_cost()
                    curr_insertion_cost = storage_manager.get_insertion_cost()
                    curr_extraction_cost = storage_manager.get_extraction_cost()

                    # Update Graphs
                    self.graphs["Fragmentation"][storage_manager.specifier()][curr_operation] += curr_fragmentation
                    self.graphs["Cost"][storage_manager.specifier()][curr_operation] += 0 if curr_cost == 0 else math.log(curr_cost)
                    self.graphs["Insertion Cost"][storage_manager.specifier()][curr_operation] += 0 if curr_insertion_cost == 0 else math.log(curr_insertion_cost)
                    self.graphs["Extraction Cost"][storage_manager.specifier()][curr_operation] += 0 if curr_extraction_cost == 0 else math.log(curr_extraction_cost)

            # Print Graphs in every repetition
            self.print_plots(repetition + 1)

    def __str__(self):
        return "Simulating a storage:\n" + \
               str(self.simulation_settings)
