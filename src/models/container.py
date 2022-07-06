"""
Container
Container is basically a set of packages
"""


class Container:
    def __init__(self, packages=None):
        if packages is None:
            packages = []
        self.packages = packages

    def add_package(self, package):
        self.packages.append(package)

    def remove_package(self, package):
        self.packages.remove(package)

    def size(self):
        total = 0
        for package in self.packages:
            total += package.size()
        return total
