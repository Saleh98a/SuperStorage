"""
Simulator Class
Runs a storage environment simulation
"""
from datetime import time
from timeit import default_timer


from random import randint

from src.models.container import Container
from src.models.order import Order
from src.models.package import Package
from src.models.product import Product

import matplotlib.pyplot as plt

from src.storage.managers.knapsack_storage_manager import KnapsackStorageManager
from src.storage.managers.naive_storage_manager import NaiveStorageManager
from src.storage.storages.super_storage import SuperStorage


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
        'Stam'
    ]

    products = []
    i = 0
    for name in product_names:
        products.append(Product(i, name, 0, randint(15, 40), 'cat'))
        i += 1
    return products


class Simulator:
    def __init__(self, simulation_settings):
        self.simulation_setting = simulation_settings
        self.graphs = {"Fragmentation": [],
                       "Cost": [],
                       "Runtime": []}
        self.curr_fragmentation = 0
        self.curr_cost = 0
        self.curr_runtime = 0

    def simulate(self):#, simulation_settings):
        products = initialize_products()
        repetitions = 100

        x_axis = range(1, 5, 2)
        for containers_num in x_axis:  # need to get from simulation settings
            self.curr_cost = 0
            self.curr_runtime = 0
            self.curr_fragmentation = 0
            print("Simulating containers number:", containers_num)
            for repetition in range(50):  # need to get from simulation settings
                storage_manager.reset_storage()
                for container in range(containers_num):
                    packages = []
                    packages_num = 40  # need to get from simulation settings
                    for package in range(packages_num):
                        shelf_size = 50  # need to get from simulation settings
                        product = products[randint(0, 99)]
                        quantity = randint(1, shelf_size // product.size)
                        p = Package(product, quantity)
                        """
                        Sample:
                        get_sample => normal(rand(0,100),rand(0,100))
                        products[1000] => int
                        quantity[1000] => int
                        Compute:
                        Total quantity (or size?) of each product
                        Divided by
                        Total quantity (or size?)
                        => Frequency (Percentage)
                        
                        
                        10*50 => 500 size  iphone 10%, 50 iphone
                        frequency => learned
                        first_rack
                        orders[1000]
                        """
                        packages.append(p)
                    c = Container(packages)
                    time1 = default_timer()
                    storage_manager.insert_container(c)
                    time2 = default_timer()
                    self.curr_runtime += (time2 - time1) / repetitions
                self.curr_fragmentation += storage_manager.get_fragmentation()
                self.curr_cost += storage_manager.get_total_cost() / repetitions
            # print("Finished repetitions with used space:", used_space)
            # need to get total_cost and space( and time later)
            # getting space:
            self.graphs["Fragmentation"].append(self.curr_fragmentation / repetitions)
            self.graphs["Cost"].append(self.curr_cost)
            self.graphs["Runtime"].append(self.curr_runtime)

        plot_graph(list(x_axis), self.graphs['Fragmentation'], 'Fragmentation', 'containers',
                   'Fragmentation Percentage', 'Fragmentation Graph')
        plot_graph(list(x_axis), self.graphs['Cost'], 'Cost', 'containers',
                   'Cost', 'Cost')
        plot_graph(list(x_axis), self.graphs['Runtime'], 'Runtime', 'containers',
                   'Runtime (sec)', 'Runtime')
        # plot_graph(list(x_axis), [used_spaces_naive, used_spaces_knap], ['naive', 'knap'], 'containers',
        #            'Fragmentation Percentage', 'Fragmentation Graph')
        # plot_graph(list(x_axis), [total_costs_naive, total_costs_knap], ['naive', 'knap'], 'containers',
        #            'Total Cost', 'Cost Graph')
        # plot_graph(list(x_axis), [total_times_naive, total_times_knap], ['naive', 'knap'], 'containers',
        #            'Runtime (seconds)', 'Runtime Graph')


def plot_graph(x_axis, y_axis, name, x_label, y_label, title):
    plt.plot(x_axis, y_axis, label=name)
    #naming the x-axis
    plt.xlabel(x_label)
    # naming the y-axis
    plt.ylabel(y_label)

    # giving a title to my graph
    plt.title(title)

    plt.legend()
    # function to show the plot
    plt.show()

# def plot_graph(x_axis, y_axis_list, y_names_list, x_label, y_label, title):
#     # plotting the points
#     for y_axis, name in zip(y_axis_list, y_names_list):
#         plt.plot(x_axis, y_axis, label=name)
#
#     # naming the x-axis
#     plt.xlabel(x_label)
#     # naming the y-axis
#     plt.ylabel(y_label)
#
#     # giving a title to my graph
#     plt.title(title)
#
#     plt.legend()
#     # function to show the plot
#     plt.show()
