"""
Utils/Helper Function for Storage
"""

def insert_naive(storage, forklift, container):
    positions_iter = iter(storage)
    for position in positions_iter:
        for package in container.packages:
            if storage.can_put_package_at(package, position):
                storage.insert_package(forklift, package, position)

def extract_naive(storage, forklift, order):
    positions_iter = iter(storage)
    for position in positions_iter:
        items_quantities = storage.get_items_at(position)
        for item in order:
            ordered_quantity = order.get_order(item)
            shelf_quantity = items_quantities.get(item, 0)
            taken_quantity = min(ordered_quantity, shelf_quantity)
            storage.extract_item(forklift, item, taken_quantity)
            order.remove_from_order(item, taken_quantity)

            if order.empty():
                return True
    return False

def insert_knapsack(storage, forklift, container):
    pass

def insert_optimized(storage, container):
    pass
