# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from simulation.simulator import Simulator
from src.storage.managers.knapsack_storage_manager import KnapsackStorageManager
from storage.managers.naive_storage_manager import NaiveStorageManager
from storage.storages.super_storage import SuperStorage


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    """
    s1 = SuperStorage()
    naive1 = NaiveStorageManager(s1)
    sim1 = Simulator()
    sim1.simulate(naive1)
    """
    #s2 = SuperStorage()
    #knapsack1 = KnapsackStorageManager(s2)
    sim2 = Simulator()
    sim2.simulate()#knapsack1)

    print_hi('success')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
