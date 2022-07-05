# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from random import randint
import numpy as np
# from scipy.stats import norm
# import scipy as scipy

from simulation.simulator import Simulator, initialize_products
from src.models.container import Container
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
    bounds = [2, 4, 7]
    manager = StorageManager(store, InsertAlgorithm.OPTIMIZED, ExtractAlgorithm.OPTIMIZED, bounds, learned_info)
    cont = Container()
    for i in range(len(learned_info)):
        print("product number", i, "frequency=", learned_info[i].frequency, "percentage=", learned_info[i].size_percentage)
    for i in range(len(learned_info)):
        pack = Package(products[i], int(1000 * learned_info[i].size_percentage))
        cont.add_package(pack)
    for package in cont.packages:
        print(" product = ", package.product.id, "quantity=", package.quantity)
    manager.insert_container(cont)
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
