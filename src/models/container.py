"""
Container
Container is basically a set of packages
"""

class Container:
    def __init__(self, packages={}):
        self.packages = packages

    def add_package(self, package):
        self.packages.add(package)

    def remove_package(self, package):
        self.packages.remove(package)