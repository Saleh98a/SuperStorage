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
        'Stam'
    ]

    products = []
    i = 0
    for name in product_names:
        products.append(Product(i, name, 0, randint(15, 40), 'cat'))  # TODO: change
        i += 1
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


class Simulator:
    def __init__(self, simulation_settings=SimulationSettings()):
        self.simulation_settings = simulation_settings
        self.graphs = {"Fragmentation": [0 for _ in range(0, 100)],
                       "Cost": [0 for _ in range(0, 100)],
                       "Runtime": [0 for _ in range(0, 100)]}
        self.curr_fragmentation = 0
        self.curr_cost = 0
        self.curr_runtime = 0
        self.storage_manager = StorageManager(SuperStorage(),  # TODO: change, maybe take it from simulation settings
                                              simulation_settings.insert,
                                              simulation_settings.extract)
        self.repetitions_num = self.simulation_settings.repetitions_num

    def reset_costs(self):
        self.curr_fragmentation = 0
        self.curr_cost = 0
        self.curr_runtime = 0

    def __str__(self):
        return "Simulating a storage:\n" + \
                str(self.simulation_settings)

    def simulate(self):
        products = initialize_products()
        containers = initialize_containers(products,
                                           self.simulation_settings.containers_num,
                                           self.simulation_settings.packages_per_container,
                                           self.simulation_settings.storage_settings.shelf_size)
        # Print data
        print(self)

        x_axis = range(0, self.simulation_settings.containers_num)
        for repetition in range(self.repetitions_num):  # need to get from simulation settings
            self.storage_manager.reset_storage()
            self.reset_costs()

            print("Inserting 100 Containers")
            for curr_container in x_axis:
                # Choose a random container
                chosen_container = randint(0, self.simulation_settings.containers_num - 1)

                # Insert the container
                time1 = default_timer()
                self.storage_manager.insert_container(containers[chosen_container])
                time2 = default_timer()

                # Update Costs
                self.curr_runtime += (time2 - time1)
                self.curr_fragmentation = self.storage_manager.get_fragmentation()
                self.curr_cost = self.storage_manager.get_total_cost()

                # Update Graphs
                self.graphs["Fragmentation"][curr_container] += self.curr_fragmentation / self.repetitions_num
                self.graphs["Cost"][curr_container] += self.curr_cost / self.repetitions_num
                self.graphs["Runtime"][curr_container] += self.curr_runtime / self.repetitions_num

        # Print Graphs
        plot_graph(title='Fragmentation Graph',
                   x_axis=list(x_axis),
                   y_axis=self.graphs['Fragmentation'],
                   x_label='Containers',
                   y_label='Fragmentation Percentage')
        plot_graph(title='Cost Graph',
                   x_axis=list(x_axis),
                   y_axis=self.graphs['Cost'],
                   x_label='Containers',
                   y_label='Cost')
        plot_graph(title='Runtime Graph',
                   x_axis=list(x_axis),
                   y_axis=self.graphs['Runtime'],
                   x_label='Containers',
                   y_label='Runtime (sec)')


def plot_graph(title, x_axis, y_axis, x_label, y_label, name=""):
    plt.plot(x_axis, y_axis, label=name)

    # naming the x-axis
    plt.xlabel(x_label)

    # naming the y-axis
    plt.ylabel(y_label)

    # giving a title to my graph
    plt.title(title)

    # If you want to add name to the slope add this line:
    # plt.legend()

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
