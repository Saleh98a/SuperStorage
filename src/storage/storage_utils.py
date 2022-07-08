"""
Utils/Helper Function for Storage
"""
from copy import copy
from time import sleep

from src.models.index import Container, SSPosition
from src.models.package import Package


def get_distance(pos1, pos2):
    return abs(pos1.row - pos2.row) + abs(pos1.col - pos2.col) + abs(pos1.shelf_num - pos2.shelf_num)


def add_position(current_path, new_pos):
    length = len(current_path)
    if length == 0:
        return [new_pos]
    elif length == 1:
        current_path.append(new_pos)
        return current_path
    else:
        min_cost = get_distance(current_path[length - 1], new_pos)
        min_cost += get_distance(new_pos, current_path[0])
        min_cost -= get_distance(current_path[length - 1], current_path[0])
        min_index = length - 1
        for i in range(length - 1):
            added_cost = get_distance(current_path[i], new_pos) + get_distance(new_pos, current_path[i + 1])
            added_cost -= get_distance(current_path[i], current_path[i + 1])
            if added_cost < min_cost:
                min_cost = added_cost
                min_index = i
        first_half = current_path[:min_index + 1]
        second_half = current_path[min_index + 1:]
        new_path = first_half + [new_pos] + second_half
        return new_path


def print_path(path):
    for pos in path:
        print("col= ", pos.col, "row=", pos.row, "height=", pos.height)


def find_optimized_path(positions):
    shortest_path = []
    for pos in positions:
        shortest_path = add_position(shortest_path, pos)
    return shortest_path


def get_path_cost(path):
    length = len(path)
    cost = get_distance(path[length - 1], path[0])
    for i in range(length - 1):
        cost += get_distance(path[i], path[i + 1])
    return cost


def insert_naive(storage, forklift, container):
    # i = 1
    # #print("new container")
    #sleep(1)
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
    for product in order:  # TODO: removing from order might cause us some problems
        for position in positions_iter:
            ordered_quantity = order.get_product_quantity(product)
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

def real_path_from_positions(positions):
    path_dict = {}
    for position in positions:
        # print(f'position {position.row} {position.col} {position.shelf_num}')
        real_position = SSPosition(position.row, position.col, 0)
        path_dict[real_position] = True
    return path_dict.keys()


# returns positions that comply with: pos.row in rows && pos.col in cols && pos.shelf in shelves
def build_territory(rows, racks, shelves):
    territory = []
    for row in rows:
        for rack in racks:
            for shelf in shelves:
                territory.append(SSPosition(row, rack, shelf))
    return territory


def insert_optimized(storage_manager, forklift, container):
    # optimization settings
    storage = storage_manager.storage
    sectors = storage_manager.sectors
    products_info = storage_manager.products_info

    # lists of packages according to where they should go
    # we should have info about current levels in storage
    priority_1 = []
    percentaged_1 = []
    percentaged_2 = []
    knapsacked = []
    for package in container.packages:
        info = products_info[package.product.id]
        # Is it prioritized? percentaged? free?
        if info.frequency >= 0.1:
            priority_1.append(package)
        elif sectors[1].get_percentage(package.product) + (package.quantity * 1.0 / sectors[1].total_size) \
                < 1.2 * info.size_percentage:
            percentaged_1.append(package)
        elif sectors[2].get_percentage(package.product) + (package.quantity * 1.0 / sectors[2].total_size) \
                < 1.2 * info.size_percentage:
            percentaged_2.append(package)
        else:
            knapsacked.append(package)

    instructions_map = {}
    insert_instruction_knapsack(storage, priority_1, sectors[0].positions, instructions_map)
    percentaged_1.extend(priority_1)  # TODO: check extreme cases
    insert_instruction_knapsack(storage, percentaged_1, sectors[1].positions, instructions_map)
    percentaged_2.extend(percentaged_1)
    insert_instruction_knapsack(storage, percentaged_2, sectors[2].positions, instructions_map)
    knapsacked.extend(percentaged_2)
    insert_instruction_knapsack(storage, knapsacked, sectors[3].positions, instructions_map)

    # Optimize path
    # path = real_path_from_positions(instructions_map.keys())
    path = instructions_map.keys()
    path = find_optimized_path(path)
    for position in path:
      for package in instructions_map[position]:
          storage.insert_package(forklift, package, position)

    return


def insert_instruction_knapsack(storage, packages, positions, instructions_map):
    for position in positions:
        packages_in_pos = knapsack_shelf(storage, packages, position)
        if len(packages_in_pos) > 0:
            instructions_map[position] = packages_in_pos
        for package in packages_in_pos:
            packages.remove(package)
    return instructions_map


def get_product_positions(product, quantity, storage_manager):
    # gets product and required amount and returns list of (position, quantity) where to get this quantity from storage
    storage_quantity = 0
    positions_quantity = []
    for sector in storage_manager.sectors:
        for position in sector.positions:
            if storage_quantity >= quantity:
                break
            current_quantity = storage_manager.storage.get_item_quantity_at(product, position)
            if current_quantity > 0:
                storage_quantity += current_quantity
                positions_quantity.append((position, current_quantity))

    if storage_quantity < quantity:
        #print("******************")
        #print("storage quantity=", storage_quantity, "product ID=", product.id)
        #print("needed quantity=", quantity)
        #print("******************")
        raise Exception("not all the order are in the sotrage,")

    first_quantity = storage_manager.storage.get_item_quantity_at(product, positions_quantity[0][0])
    while first_quantity <= (storage_quantity - quantity):
        storage_quantity -= first_quantity
        positions_quantity.pop(0)
        first_quantity = storage_manager.storage.get_item_quantity_at(product, positions_quantity[0][0])
    pos = positions_quantity[0][0]
    quantity = positions_quantity[0][1] - (storage_quantity - quantity)
    positions_quantity.pop(0)
    positions_quantity = [(pos, quantity)] + positions_quantity
    return positions_quantity


def extract_optimized(storage_manager, forklift, order):
    position_actions = {}
    for product in order.item_orders:
        positions_quantity = get_product_positions(product, order.item_orders[product], storage_manager)
        for (position, quantity) in positions_quantity:
            if position in position_actions.keys():
                position_actions[position].append((product, quantity))
            else:
                position_actions[position] = [(product, quantity)]
    positions = list(position_actions.keys())
    path = find_optimized_path(positions)
    for position in path:
        for (product, quantity) in position_actions[position]:
            storage_manager.storage.extract_product(forklift, product, quantity, position)

    for sector in storage_manager.sectors:
        for position in sector.positions:
            if position in position_actions.keys():
                for (product, quantity) in position_actions[position]:
                    sector.remove_from_sector(product, quantity)

    # TODO: remove the code below' this is just for tests
    storage_quantity = [0 for _ in range(100)]
    for row in storage_manager.storage.racks:
        for rack in row:
            for shelf in rack.shelves:
                for product in shelf.item_quantities.keys():
                    storage_quantity[product.id] += shelf.item_quantities[product]
    #print("extraction completed successfully")
    #print("#printing all quantities in our storage after the extraction")
    all_products_quantity = 0
    for i in range(len(storage_quantity)):
        # #print("product ID=", i, "storage quantity=", storage_quantity[i])
        all_products_quantity += storage_quantity[i]
    #print("#printing quantity of all products in storage:-")
    #print(all_products_quantity)


def knapsack_shelf(storage, packages, position):
    shelf = storage.get_shelf(position)
    free_size = shelf.size - shelf.used_size
    memo = [Container() for _ in range(free_size + 1)]
    for i in range(1, free_size + 1):
        max_used = memo[i - 1].size()
        like_previous = True
        for package in packages:
            if package.size() <= i and package not in memo[i - package.size()].packages:
                if package.size() + memo[i - package.size()].size() > max_used:
                    like_previous = False
                    max_used = package.size() + memo[i - package.size()].size()
                    memo[i].packages = copy(memo[i - package.size()].packages)
                    memo[i].add_package(package)
        if like_previous:
            memo[i] = memo[i - 1]
    return memo[free_size].packages
