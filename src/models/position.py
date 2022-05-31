"""
Position models
Describe position inside the storage
"""

from abc import ABC, abstractmethod

class Position(ABC):
    # empty class
    def __init__(self):
        pass

class SSPosition(Position):
    def __init__(self, row, col, shelf_num):
        super().__init__()
        self.row = row
        self.col = col
        self.shelf_num = shelf_num
