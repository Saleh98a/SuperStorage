"""
Forklift models
Describe forklift moving packages/containers inside the storage
"""
import math
from abc import ABC
from position import SSPosition

class Forklift(ABC):
    # empty class
    def __init__(self):
        pass

class SSForklift:
    def __init__(self, position=SSPosition(0, 0, 0), weight_limit=math.inf, size_limit=math.inf, vertical_coeff=1, horizontal_coeff=1):
        super.__init__()
        self.position = position
        self.weight_limit = weight_limit
        self.size_limit = size_limit
        self.vertical_coeff = vertical_coeff
        self.horizontal_coeff = horizontal_coeff

