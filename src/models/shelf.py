"""
Shelf model
Shelf has a size and can hold a number of packages
"""

import math

class Shelf:
    def __init__(self, size, weight_limit=math.inf):
        self.size = size
        self.used_size = 0
        self.packages = {}

    def put_package(self, package):
        if not self._can_put_package(package):
            raise Exception("Package can't fit on this shelf")
        self.used_size += package.size
        self.packages.add(package)

    def remove_package(self, package):
        if package not in self.packages:
            raise Exception("The package isn't on this shelf")
        self.used_size -= package.size
        self.packages.remove(package)

    def _can_put_package(self, package):
        return  package.size + self.used_size <= self.size
