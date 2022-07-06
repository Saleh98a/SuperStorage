"""
Simulation Settings models
setting configurations of a given simulation
"""

from enum import Enum
from src.storage.storages.storage_settings import StorageSettings


class InsertAlgorithm(Enum):
    NAIVE = 1
    KNAPSACK = 2
    OPTIMIZED = 3


class ExtractAlgorithm(Enum):
    NAIVE = 1
    OPTIMIZED = 2


class SimulationSettings:
    def __init__(self,
                 insert_algo=InsertAlgorithm.NAIVE,
                 extract_algo=ExtractAlgorithm.NAIVE,
                 storage_settings=StorageSettings(),
                 insertion_only=True,
                 interlapping=False,
                 repetitions_num=30,
                 containers_num=100,
                 packages_per_container=40):
        self.storage_settings = storage_settings
        self.insert = insert_algo
        self.extract = extract_algo
        self.insertion_only = insertion_only
        self.interlapping = interlapping
        self.repetitions_num = repetitions_num
        self.containers_num = containers_num
        self.packages_per_container = packages_per_container

    def __str__(self):
        return str(self.storage_settings) + \
               "Repetitions Num: " + str(self.repetitions_num) + "\n" + \
               "Containers Num: " + str(self.containers_num) + "\n" + \
               "Packages Per Container: " + str(self.packages_per_container)


"""
what parameters we need ?!
    1.insert algorithm
    2.extract algorithm
3 kinds of simulations
1. just insert
2. insert and extract (not interlapping)
3. insert and extract (interlapping)
"""
