"""
Simulation Settings models
setting configurations of a given simulation
"""

from enum import Enum

from src.storage.managers.storage_manager_settings import StorageManagerSettings
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
                 storage_managers_settings=None,
                 storage_settings=StorageSettings(),
                 exponential_scale=20,
                 extraction_probability=0.5,
                 insertion_headstart=5,
                 repetitions_num=1,
                 operations_num=100,
                 packages_per_container=40,
                 products_per_order=5,
                 insert_lambda_coeff=1,
                 extract_lambda_coeff=1,
                 export=False):
        if storage_managers_settings is None:
            storage_managers_settings = [
                StorageManagerSettings(InsertAlgorithm.NAIVE, ExtractAlgorithm.NAIVE)
            ]
        self.storage_managers_settings = storage_managers_settings
        self.storage_settings = storage_settings
        self.exponential_scale = exponential_scale
        self.extraction_probability = extraction_probability
        self.repetitions_num = repetitions_num
        self.operations_num = operations_num
        self.packages_per_container = packages_per_container
        self.products_per_order = products_per_order
        self.insertion_headstart = insertion_headstart
        self.insert_lambda_coeff = insert_lambda_coeff
        self.extract_lambda_coeff = extract_lambda_coeff
        self.export = export

    def __str__(self):

        return "storage_managers_settings: \n" + '\n'.join([str(e) for e in self.storage_managers_settings]) + "\n" + \
               "storage_settings: " + str(self.storage_settings) + "\n" + \
               "extraction_probability: " + str(self.extraction_probability) + "\n" + \
               "operations_num: " + str(self.operations_num) + "\n" + \
               "packages_per_container: " + str(self.packages_per_container) + "\n" + \
               "products_per_order: " + str(self.products_per_order) + "\n" + \
               "insertion_headstart: " + str(self.insertion_headstart) + "\n" + \
               "insert_lambda_coeff: " + str(self.insert_lambda_coeff) + "\n" + \
               "extract_lambda_coeff: " + str(self.extract_lambda_coeff) + "\n" + \
               "repetitions_num: " + str(self.repetitions_num) + "\n" + \
               "export: " + str(self.export) + "\n"

