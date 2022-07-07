# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from random import randint
import numpy as np
# from scipy.stats import norm
# import scipy as scipy

from simulation.simulator import Simulator, initialize_products
from src.models.container import Container
from src.models.order import Order
from src.models.package import Package

from src.simulation.simulation_settings import SimulationSettings, InsertAlgorithm, ExtractAlgorithm
from src.storage.managers.storage_manager import learn, StorageManager
from src.storage.storages.super_storage import SuperStorage


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    products = initialize_products()
    learned_info = learn(products, 100000)
    store = SuperStorage()
    bounds = [2, 8, 14]
    manager = StorageManager(store, InsertAlgorithm.OPTIMIZED, ExtractAlgorithm.OPTIMIZED, bounds, learned_info)
    for i in range(10):
        first_container = Container()
        second_container = Container()
        third_container = Container()
        first_order = Order()
        second_order = Order()
        for product in products:
            first_container.add_package(Package(product, 3))
            second_container.add_package(Package(product, 5))
            third_container.add_package(Package(product, 2))
            first_order.add_to_order(product, 5)
            second_order.add_to_order(product, 5)
        manager.insert_container(first_container)
        manager.insert_container(second_container)
        manager.extract_order(first_order)
        if i % 2:
            manager.extract_order(second_order)
        manager.insert_container(third_container)
    sim2 = Simulator(SimulationSettings(insert_algo=InsertAlgorithm.KNAPSACK,
                                        extract_algo=ExtractAlgorithm.NAIVE))
    sim2.simulate()
    """
    """
    """
    s2 = SuperStorage()
    knapsack1 = KnapsackStorageManager(s2)
    sim2 = Simulator()
    sim2.simulate(knapsack1)
    """
    print_hi('It\'s Chewsday Innit')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# def learn(products) => updates the frequency/percentage/....
