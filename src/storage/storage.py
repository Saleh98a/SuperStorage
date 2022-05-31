"""
Storage class/interface
"""

from abc import ABC, abstractmethod

class Storage(ABC):

    @abstractmethod
    def insert_package(self, forklift, container, position):
        pass

    @abstractmethod
    def extract_item(self, forklift, item, quantity, position):
        pass

    @abstractmethod
    def calculate_forklift_cost(self, forklift, position):
        pass

    @abstractmethod
    def move_forklift(self, forklift, position):
        pass

    @abstractmethod
    def get_forklift_position(self, forklift, position):
        pass