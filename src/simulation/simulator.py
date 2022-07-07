"""
Simulator Class
Runs a storage environment simulation
"""
from timeit import default_timer

from random import randint

from src.models.container import Container
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
        products.append(Product(i, name, 0, randint(10, 30), 'cat'))  # TODO: change quantity and category
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
        self.containers_num = self.simulation_settings.containers_num
        self.repetitions_num = self.simulation_settings.repetitions_num
        # self.graphs = {'Fragmentation': [0 for _ in range(0, self.containers_num)],
        #                'Cost': [0 for _ in range(0, self.containers_num)],
        #                'Runtime': [0 for _ in range(0, self.containers_num)]}
        self.curr_fragmentation = 0
        self.curr_cost = 0
        self.curr_runtime = 0

        self.storage_managers = []
        self.graphs = {'Fragmentation': {},
                       'Cost': {},
                       'Runtime': {}}
        for insert in simulation_settings.insert:
            for extract in simulation_settings.extract:
                # TODO: change SuperStorage(), maybe take it from simulation settings
                storage_manager = StorageManager(SuperStorage(), insert, extract)
                self.storage_managers.append(storage_manager)
                # print(storage_manager.specifier())
                for graph in self.graphs:
                    self.graphs[graph][storage_manager.specifier()] = [0 for _ in range(0, self.containers_num)]

        # plt.ion()

    def create_graph(self, curr_ax, x, ylist, ynames, ylabel):
        for y, yname in zip(ylist, ynames):
            curr_ax.plot(x, y, label=yname)
        curr_ax.set(ylabel=ylabel)
        curr_ax.label_outer()
        curr_ax.set_xlim([1, self.containers_num])  # TODO: change to containers num

    def print_plots(self, repetition):
        fig = plt.figure()
        axs = []
        i = 1
        for graph_name in self.graphs:
            axs.append(fig.add_subplot(3, 1, i))
            self.create_graph(axs[-1],
                              list(range(1, self.containers_num + 1)),
                              # Calculates average over repetitions
                              [[y / repetition for y in self.graphs[graph_name][manager]] for manager in self.graphs[graph_name]],
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
        products = initialize_products()
        containers = initialize_containers(products,
                                           self.simulation_settings.containers_num,
                                           self.simulation_settings.packages_per_container,
                                           self.simulation_settings.storage_settings.shelf_size)
        # Print data
        print(self)

        for repetition in range(self.repetitions_num):  # need to get from simulation settings
            for storage_manager in self.storage_managers:
                storage_manager.reset_storage()
            self.reset_costs()

            print("Inserting 100 Containers")
            for curr_container in range(0, self.containers_num):
                # Choose a random container
                chosen_container = randint(0, self.containers_num - 1)

                for storage_manager in self.storage_managers:
                    # Insert the container
                    time1 = default_timer()
                    storage_manager.insert_container(containers[chosen_container])
                    time2 = default_timer()

                    # Update Costs
                    self.curr_runtime += (time2 - time1)
                    self.curr_fragmentation = storage_manager.get_fragmentation()
                    self.curr_cost = storage_manager.get_total_cost()

                    # Update Graphs
                    self.graphs["Fragmentation"][storage_manager.specifier()][curr_container] += self.curr_fragmentation
                    self.graphs["Cost"][storage_manager.specifier()][curr_container] += self.curr_cost
                    self.graphs["Runtime"][storage_manager.specifier()][curr_container] += self.curr_runtime

            # Print Graphs in every repetition
            self.print_plots(repetition + 1)

    def __str__(self):
        return "Simulating a storage:\n" + \
               str(self.simulation_settings)
