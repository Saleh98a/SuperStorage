"""
Simulator Class
Runs a storage environment simulation
"""
import math
import random
from random import randint
import numpy as np
import matplotlib.pyplot as plt

from src.models.container import Container
from src.models.order import Order
from src.models.package import Package
from src.models.product import Product, ProductInfo

from src.storage.managers.storage_manager import StorageManager
from src.storage.storages.super_storage import SuperStorage
from src.simulation.simulation_settings import SimulationSettings


def initialize_products():
    product_names = [
        'Television',
        'Table',
        'Chair',
        'Book',
        'Coffee',
        'Water',
        'Bottle',
        'Vacuum',
        'Paint',
        'Video game',
        'Board game',
        'Plant',
        'Patio furniture',
        'Door',
        'Door knob',
        'Security system',
        'Sign',
        'Off-brand accessory',
        'Casual clothing',
        'High-end clothing',
        'Computer',
        'Computer part',
        'Monitor',
        'Glasses',
        'Sticky notes',
        'Pens',
        'Pencils',
        'Paper',
        'Cards',
        'Knives',
        'Light bulb',
        'Music',
        'Glass',
        'Windows',
        'Wood',
        'Napkins',
        'Silverware',
        'Sun reflectors',
        'Towels',
        'Bikes',
        'Car accessories',
        'Headphones',
        'Music players',
        'Tea',
        'Pre-prepared food',
        'Skateboard',
        'Cell phone',
        'Cell phone accessories',
        'Jewelry',
        'Rug',
        'Wall decal',
        'Painting',
        'Reprinted artwork',
        'Sports paraphernalia',
        'Television paraphernalia',
        'Movie paraphernalia',
        '3D glasses/headsets',
        'Sound systems',
        'Shoes',
        'Hat',
        'Helmet',
        'Keychain',
        'Bookend',
        'Frame',
        'Coloring book',
        'Pillow',
        'Bedsheet',
        'Wallet',
        'Money clip',
        'Toy',
        'Clock',
        'Gag gift',
        'Sculpture',
        'Candle',
        'Cleaning supplies',
        'Canvas',
        'Bean bag chair',
        'Back support attachments for chairs',
        'Wheelchair',
        'Parts for discontinued electronics',
        'Weight loss product',
        'Scale',
        'Shower curtain',
        'Toothbrush',
        'Toilet seat covers',
        'Tattoo gun',
        'Hair care product',
        'Makeup',
        'Gun',
        'Poster',
        'Fabric',
        'Pharmaceuticals',
        'Movie',
        'GPS locator',
        'Car',
        'Ticket',
        'Piping',
        'Tool',
        'Weights',
        'Airpods'
    ]

    products = []
    for i in range(len(product_names)):
        products.append(Product(i, product_names[i], 0, randint(10, 30), 'cat'))  # TODO: change weight and category
    return products


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


def draw_order(products):
    """
    Distributions:
        - Each product quantity: Poisson Distribution
            Parameter: Lambda = quantities_lambda[i] (Chosen randomly from 1-5 incl.)

        - Picking the product: Exponential Distribution (not critical)
            Parameter: Lambda = exponential_lambda (Chosen randomly from 30-80 incl.)


    """
    quantity_lambda_list = [3 for _ in range(len(products))]  # TODO revert this to randint(1,5)
    exponential_lambda = 40  # TODO revert this to randint(30,80)
    order_len = np.random.randint(1, 50)

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



def draw_container(products, package_max_size):
    """
    Distributions:
        - Each product quantity: Poisson Distribution
            Parameter: Lambda = quantities_lambda[i] (Chosen randomly from 1-5 incl.)

        - Picking the product: Exponential Distribution (not critical)
            Parameter: Lambda = exponential_lambda (Chosen randomly from 30-80 incl.)


    """
    quantity_lambda_list = [60 for _ in range(len(products))]  # TODO revert this to randint(...)
    exponential_lambda = 40  # TODO revert this to randint(30,80)
    container_len = np.random.randint(1, 50)

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
    total_size_of_product = [0 for _ in range(products_num)]
    total_orders_of_product = [0 for _ in range(products_num)]
    for order in orders:
        current_order_products = [False for _ in range(products_num)]
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
        self.containers_num = self.simulation_settings.containers_num
        self.repetitions_num = self.simulation_settings.repetitions_num
        self.curr_fragmentation = 0
        self.curr_cost = 0
        self.curr_runtime = 0

        self.products = initialize_products()
        self.learned_info = learn(self.products, 500)

        self.storage_managers = []
        self.graphs = {
            'Fragmentation': {},
            'Cost': {}
        }
        for insert in simulation_settings.insert:
            for extract in simulation_settings.extract:
                # TODO: change SuperStorage(), maybe take it from simulation settings
                storage_manager = StorageManager(SuperStorage(self.simulation_settings.storage_settings),
                                                 insert,
                                                 extract,
                                                 [2, 5, 8],
                                                 self.learned_info)
                self.storage_managers.append(storage_manager)
                for graph in self.graphs:
                    self.graphs[graph][storage_manager.specifier()] = [0 for _ in range(0, self.containers_num)]

        # plt.ion()

    def create_graph(self, curr_ax, x, ylist, ynames, ylabel):
        for y, yname in zip(ylist, ynames):
            curr_ax.plot(x, y, label=yname)
        curr_ax.set(ylabel=ylabel)
        curr_ax.label_outer()
        curr_ax.set_xlim([1, self.containers_num])  # TODO: check why doesnt work on 1

    def print_plots(self, repetition):
        fig = plt.figure()
        axs = []
        i = 1
        for graph_name in self.graphs:
            axs.append(fig.add_subplot(3, 1, i))
            self.create_graph(axs[-1],
                              list(range(1, self.containers_num + 1)),
                              # Calculates average over repetitions
                              [[y / repetition for y in self.graphs[graph_name][manager]] for manager in
                               self.graphs[graph_name]],
                              [manager for manager in self.graphs[graph_name]],
                              graph_name)
            i += 1

        # Give title for 1st Graph
        axs[0].set_title('Repetitions = ' + str(repetition))

        # Give xlabel for last Graph
        axs[-1].set(xlabel='Containers')

        plt.ion()
        plt.legend()
        plt.show(block=False)

    def reset_costs(self):
        self.curr_fragmentation = 0
        self.curr_cost = 0
        self.curr_runtime = 0

    def simulate(self):
        # Print data
        print(self)

        extraction_probability = 0.05

        for repetition in range(self.repetitions_num):  # need to get from simulation settings
            for storage_manager in self.storage_managers:
                storage_manager.reset_storage()
            self.reset_costs()

            for curr_container in range(0, self.containers_num):
                # Choose a random container
                chosen_container = draw_container(products=self.products, package_max_size=self.simulation_settings.storage_settings.shelf_size)
                chosen_order = draw_order(products=self.products)
                is_extract = random.random() <= extraction_probability

                for storage_manager in self.storage_managers:
                    # Insert the container
                    if not is_extract:
                        storage_manager.insert_container(chosen_container)
                    else:
                        order = fix_order(storage_manager.storage, chosen_order)
                        storage_manager.extract_order(order)

                    # Update Costs
                    self.curr_fragmentation = storage_manager.get_fragmentation()
                    self.curr_cost = storage_manager.get_total_cost()

                    # Update Graphs
                    self.graphs["Fragmentation"][storage_manager.specifier()][curr_container] += self.curr_fragmentation
                    self.graphs["Cost"][storage_manager.specifier()][curr_container] += self.curr_cost

            # Print Graphs in every repetition
            self.print_plots(repetition + 1)

    def __str__(self):
        return "Simulating a storage:\n" + \
               str(self.simulation_settings)
