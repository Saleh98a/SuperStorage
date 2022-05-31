"""
Rack model (Rack is basically a list of shelves)
"""

from shelf import Shelf

class Rack:
    def __init__(self, num_of_shelves, shelf_size):
        self.shelves = [Shelf(shelf_size) for i in range(num_of_shelves)]

    def add_shelf(self, shelf):
        self.shelves.append(shelf)

    def remove_shelf(self, shelf):
        self.shelves.remove(shelf)
