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

    def __str__(self):
        if self is InsertAlgorithm.NAIVE:
            return "Insert:Naive"
        if self is InsertAlgorithm.KNAPSACK:
            return "Insert:Knapsack"
        if self is InsertAlgorithm.OPTIMIZED:
            return "Insert:Optimized"
        else:
            raise Exception("Undefined InsertAlgorithm")


class ExtractAlgorithm(Enum):
    NAIVE = 1
    OPTIMIZED = 2

    def __str__(self):
        if self is ExtractAlgorithm.NAIVE:
            return "Extract:Naive"
        if self is ExtractAlgorithm.OPTIMIZED:
            return "Extract:Optimized"
        else:
            raise Exception("Undefined ExtractAlgorithm")


class SimulationSettings:
    def __init__(self,
                 insert_algo=None,
                 extract_algo=None,
                 storage_settings=StorageSettings(),
                 insertion_only=True,
                 extraction_probability=0.5,
                 repetitions_num=30,
                 operations_num=100,
                 packages_per_container=40,
                 products_per_order=5):
        if insert_algo is None:
            insert_algo = [InsertAlgorithm.NAIVE, InsertAlgorithm.KNAPSACK]#, InsertAlgorithm.OPTIMIZED]
        if extract_algo is None:
            extract_algo = [ExtractAlgorithm.NAIVE]#, ExtractAlgorithm.OPTIMIZED]
        self.storage_settings = storage_settings
        self.insert = insert_algo
        self.extract = extract_algo
        self.insertion_only = insertion_only
        self.extraction_probability = extraction_probability
        self.repetitions_num = repetitions_num
        self.operations_num = operations_num
        self.packages_per_container = packages_per_container
        self.products_per_order = products_per_order

    def __str__(self):
        return str(self.storage_settings) + \
               "Repetitions Num: " + str(self.repetitions_num) + "\n" + \
               "Operations per Simulation Num: " + str(self.operations_num) + "\n" + \
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
