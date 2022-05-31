"""
Our Storage Implementation
"""

from storage import Storage

class SuperStorage(Storage):

    def __int__(self, num_of_racks=100, shelves_per_rack=10, weight_per_rack=10, rack_size=2):
        super().__init__()
        self.num_of_racks = num_of_racks
        self.shelves_per_rack = shelves_per_rack
        self.weight_per_rack = weight_per_rack
        self.rack_size = rack_size

    def insert_package(self, forklift, container, position):
        
        pass

    def extract_item(self, forklift, item, quantity, position):
        pass

    def calculate_forklift_cost(self, forklift, position):
        pass

    def move_forklift(self, forklift, position):
        pass

    def get_forklift_position(self, forklift, position):
        pass