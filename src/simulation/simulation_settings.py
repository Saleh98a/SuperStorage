"""
Simulation Settings models
setting configurations of a given simulation
"""

from enum import Enum

""""

*****************************
WE DON'T NEED THIS SHIT !!!!!
*****************************

class InsertAlgorithm(Enum):
    NAIVE = 1
    KNAPSACK = 2


class ExtractAlgorithm(Enum):
    NAIVE = 1

"""


class SimulationSettings:
    def __init__(self, storage_settings, insert_algo, extract_algo, insertion_only, interlapping):
        self.storage_settings = storage_settings
        self.insert = insert_algo
        self.extract = extract_algo
        self.insertion_only = insertion_only
        self.interlapping = interlapping


"""
what parameters we need ?!
    1.insert algorithm
    2.extract algorithm
3 kinds of simulations
1. just insert
2. insert and extract (not interlapping)
3. insert and extract (interlapping)
"""
