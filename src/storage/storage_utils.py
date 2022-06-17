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
    for position in positions_iter:
        items_quantities = storage.get_items_at(position)
        for product in order:
            ordered_quantity = order.get_order(product)
            shelf_quantity = items_quantities.get(product, 0)
            taken_quantity = min(ordered_quantity, shelf_quantity)
            storage.extract_product(forklift, product, taken_quantity, position)
            order.remove_from_order(product, taken_quantity)
            if order.empty():
                return True
    return False


def insert_knapsack(storage, forklift, container):
    pass


def insert_optimized(storage, container):
    pass
