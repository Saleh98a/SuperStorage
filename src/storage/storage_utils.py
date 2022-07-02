"""
Utils/Helper Function for Storage
"""
from copy import copy
from src.models.index import Container, SSPosition

def insert_naive(storage, forklift, container):
    #i = 1
    #print("new container")
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
    for product in order: # TODO: removing from order might cause us some problems
        for position in positions_iter:
            ordered_quantity = order.get_order(product)
            current_quantity = storage.get_item_quantity_at(product, position)
            quantity_to_extract = min(ordered_quantity, current_quantity)
            extracted_quantity = storage.extract_product(forklift, product, quantity_to_extract, position)
            order.remove_from_order(product, extracted_quantity)
            if extracted_quantity == ordered_quantity:
                break
    return order.empty()


def insert_knapsack(storage, forklift, container):
    cont = Container()
    cont.packages = copy(container.packages)
    positions_iter = iter(storage)
    for position in positions_iter:
        if cont.size() == 0:
            return True
        packages_to_insert = knapsack_shelf(storage, cont.packages, position)
        for package in packages_to_insert:
            cont.remove_package(package)
            storage.insert_package(forklift, package, position)
    return False

def extract_modified(storage, forklift, order):
    pass

def insert_optimized(storage, forklift, container):
    # default optimization settings
    priority_one_pos = [[[
        SSPosition(row, rack, shelf)
        for shelf in range(0, storage.shelves_per_rack)]
        for rack in range(0, 1)]
        for row in range(0, 1)]
    priority_two_pos = [[[
        SSPosition(row, rack, shelf)
        for shelf in range(0, storage.shelves_per_rack)]
        for rack in range(1, 3)]
        for row in range(1, 3)]
    priority_three_pos = [[[
        SSPosition(row, rack, shelf)
        for shelf in range(0, storage.shelves_per_rack)]
        for rack in range(3, 5)]
        for row in range(3, 5)]
    percentaged_one_pos = [[[
        SSPosition(row, rack, shelf)
        for shelf in range(0, storage.shelves_per_rack)]
        for rack in range(5, 7)]
        for row in range(5, 7)]
    percentaged_two_pos = [[[
        SSPosition(row, rack, shelf)
        for shelf in range(0, storage.shelves_per_rack)]
        for rack in range(7, 9)]
        for row in range(7, 9)]
    free_area_pos = [[[
        SSPosition(row, rack, shelf)
        for shelf in range(0, storage.shelves_per_rack)]
        for rack in range(9, storage.racks_per_row)]
        for row in range(9, storage.rows)]
    # lists of packages according to where they should go
    # we should have info about current levels in storage
    priority_1 = []
    priority_2 = []
    priority_3 = []
    percentaged_1 = []
    percentaged_2 = []
    kanpsacked = []
    for package in container.packages:
        break
        # Is it prioritized?
        #   priority_1.append(package) Add it to one of the priority zones
        #   priority_2.append(package) Add it to one of the priority zones
        #   priority_3.append(package) Add it to one of the priority zones
        # Goes to percentaged section?
        #   percentaged_1.append(package) (if it allows saving proper percentages in percentaged level 1)
        #   percentaged_2.append(package) (if it allows saving proper percentages in percentaged level 2)
        # Knapsack them kids
        #   kanpsacked.append(package)

    # TODO: territory class? with iterator over its positions

    instructions_map = {}
    insert_instruction_knapsack(storage, priority_1, priority_one_pos, instructions_map)
    insert_instruction_knapsack(storage, priority_2, priority_two_pos, instructions_map)
    insert_instruction_knapsack(storage, priority_3, priority_three_pos, instructions_map)
    insert_instruction_knapsack(storage, percentaged_1, percentaged_one_pos, instructions_map)
    insert_instruction_knapsack(storage, percentaged_2, percentaged_two_pos, instructions_map)
    insert_instruction_knapsack(storage, kanpsacked, free_area_pos, instructions_map)

    # Optimize path
    positions_on_path = instructions_map.keys()
    # path = optimize_path(positions_on_path)
    # for position in path:
    #   for package in instructions_map[position]:
    #       insert package to position

    return

def insert_instruction_knapsack(storage, packages, positions, instructions_map={}):
    for row in positions:
        for rack in row:
            for position in rack:
                packages_in_pos = instructions_map[position] = knapsack_shelf(storage, packages, position)
                for package in packages_in_pos:
                    packages.remove(package)
    return instructions_map

def knapsack_shelf(storage, packages, position):
    shelf = storage.get_shelf(position)
    free_size = shelf.size-shelf.used_size
    memo = [Container() for _ in range(free_size + 1)]
    for i in range(1, free_size+1):
        max_used = memo[i-1].size()
        like_previous = True
        for package in packages:
            if package.size() <= i and package not in memo[i-package.size()].packages:
                if package.size() + memo[i-package.size()].size() > max_used:
                    like_previous = False
                    max_used = package.size() + memo[i-package.size()].size()
                    memo[i].packages = copy(memo[i-package.size()].packages)
                    memo[i].add_package(package)
        if like_previous:
            memo[i] = memo[i-1]
    return memo[free_size].packages