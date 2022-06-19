"""
Utils/Helper Function for Storage
"""
import copy

from src.models.container import Container


def insert_naive(storage, forklift, container):
    i = 1
    print("new contaner")
    for package in container.packages:
        success = False
        positions_iter = iter(storage)
        for position in positions_iter:
            if storage.can_put_package_at(package, position):
                success = True
                storage.insert_package(forklift, package, position)
                break
        if not success:
            raise Exception("Couldn't insert package: " + str(package))


def extract_naive(storage, forklift, order):
    positions_iter = iter(storage)
    for product in order:
        for position in positions_iter:
            ordered_quantity = order.get_order(product)
            taken_quantity = storage.extract_product(forklift, product, ordered_quantity, position)
            order.remove_from_order(product, taken_quantity)
            if taken_quantity == ordered_quantity:
                break
        if order.empty():
            return True
    return False


def insert_knapsack(storage, forklift, container):
    cont = Container()
    cont.packages = copy.copy(container.packages)
    positions_iter = iter(storage)
    for position in positions_iter:
        if cont.size() == 0:
            return True
        knapsack_shelf(storage, forklift, cont, storage.get_shelf(position), position)
    return False

def extract_modified(storage, forklift, order):
    pass


def insert_optimized(storage, container):
    pass


def knapsack_shelf(storage, forklift, container, shelf, position):
    free_size = shelf.size-shelf.used_size
    memo = [Container() for i in range(free_size + 1)]
    for i in range(1, free_size+1):
        max_used = memo[i-1].size()
        like_previous = True
        for package in container.packages:
            if package.size() <= i and package not in memo[i-package.size()].packages:
                if package.size() + memo[i-package.size()].size() > max_used:
                    like_previous = False
                    max_used = package.size() + memo[i-package.size()].size()
                    memo[i].packages = copy.copy(memo[i-package.size()].packages)
                    memo[i].add_package(package)
        if like_previous:
            memo[i] = memo[i-1]
    for package in memo[free_size].packages:
        container.remove_package(package)
        storage.insert_package(forklift, package, position)
