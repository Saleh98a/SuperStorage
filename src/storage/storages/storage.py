"""
Storage class/interface
"""

from abc import ABC, abstractmethod

class Storage(ABC):

    @abstractmethod
    def insert_package(self, forklift, package, position):
        pass

    @abstractmethod
    def extract_product(self, forklift, product, quantity, position):
        pass

    @abstractmethod
    def calculate_forklift_cost(self, forklift, position):
        pass

    @abstractmethod
    def move_forklift(self, forklift, position):
        pass

    @abstractmethod
    def get_items_at(self, position):
        pass

    @abstractmethod
    def get_item_quantity_at(self, item, position):
        pass

    @abstractmethod
    def can_put_package_at(self, package, position):
        pass

    @abstractmethod
    def print(self):
        pass
