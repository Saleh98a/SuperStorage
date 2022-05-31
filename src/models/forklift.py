"""
Forklift models
Describe forklift moving packages/containers inside the storage
"""

from abc import ABC, abstractmethod

class Forklift(ABC):
    # empty class
    def __init__(self):
        pass

class SSForklift:
    def __init__(self, position, weight_limit, size_limit, vertical_coeff, horizontal_coeff):
        self.position = position
        self.weight_limit = weight_limit
        self.size_limit = size_limit
        self.vertical_coeff = vertical_coeff
        self.horizontal_coeff = horizontal_coeff

