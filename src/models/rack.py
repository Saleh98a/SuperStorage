"""
Rack model (Rack is basically a list of shelves)
"""

class Rack:
    def __init__(self, shelves=[]):
        self.shelves = shelves

    def add_shelf(self, shelf):
        self.shelves.append(shelf)

    def remove_shelf(self, shelf):
        self.shelves.remove(shelf)
