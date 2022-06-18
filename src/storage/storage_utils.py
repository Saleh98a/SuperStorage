"""
Utils/Helper Function for Storage
"""


def insert_naive(storage, forklift, container):
    positions_iter = iter(storage)
    for package in container.packages:
        success = False
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
    pass


def insert_optimized(storage, container):
    pass
