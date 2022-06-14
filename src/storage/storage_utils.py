"""
Utils/Helper Function for Storage
"""

def insert_naive(storage, container):
    positions_iter = iter(storage)
    for position in positions_iter:
        for package in container.packages:
            if storage.can_put_package_at(package, position):
                storage.insert_package(package)

def extract_naive(storage, order):
    pass

def insert_knapsack(storage, container):
    pass

def insert_optimized(storage, container):
    pass
