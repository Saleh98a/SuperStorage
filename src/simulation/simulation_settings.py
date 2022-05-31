"""
Simulation Settings models
setting configurations of a given simulation
"""

from enum import Enum

class InsertAlgorithm(Enum):
    NAIVE = 1
    KNAPSACK = 2

class ExtractAlgorithm(Enum):
    NAIVE = 1

class SimulationSettings:
    def __init__(self, insert_settings, extract_settings, interlapping, operation_order):
        self.insert_settings = insert_settings
        self.extract_settings = extract_settings
        self.interlapping = interlapping
        self.operation_order = operation_order

