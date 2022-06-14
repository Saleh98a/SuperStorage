"""
Rack model (Rack is basically a list of shelves)
"""

from shelf import Shelf

class Rack:
    def __init__(self, num_of_shelves, shelf_size):
        self.num_of_shelves = num_of_shelves
        self.shelf_size = shelf_size
        self.shelves = [Shelf(shelf_size) for _ in range(num_of_shelves)]
