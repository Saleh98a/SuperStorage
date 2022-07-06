"""
Utils/Helper Function for Storage
"""
from copy import copy
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
    # print("new container")
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


# returns positions that comply with: pos.row in rows && pos.col in cols && pos.shelf in shelves
def build_territory(rows, racks, shelves):
    territory = []
    for row in rows:
        for rack in racks:
            for shelf in shelves:
                territory.append(SSPosition(row, rack, shelf))
    return territory


def insert_optimized(storage_manager, forklift, container):
    storage = storage_manager.storage
    products_info = storage_manager.products_info
    top_level_percentage = storage_manager.top_level_percentage
    sectors = storage_manager.sectors
    positions_actions = {}  # packages to insert in each position
    current_sector_packages = []    # packages of current sector
    packages_to_remove = []         # packages that need to remove from container
    updated_packages = []
    # TODO: remove the shit below from the code this is just for testing
    print("insert started -")
    first_sector_packs_num = 0
    second_and_third_sector_packs_num = 0
    last_sector_packs_num = 0
    # first_stage:- check for top frequency products - Sector 1
    for package in container.packages:
        product = package.product
        total_quantity = package.quantity
        if top_level_percentage[product.id] > 0:
            current_percent = sectors[0].get_percentage(product)
            max_percent = top_level_percentage[product.id]
            max_add_quantity = int((max_percent - current_percent) * sectors[0].total_size)
            if current_percent < max_percent and max_add_quantity > 0:
                quantity_to_add = max_add_quantity
                if max_add_quantity >= total_quantity:
                    quantity_to_add = total_quantity
                    packages_to_remove.append(package)
                else:
                    updated_package = Package(product, total_quantity - quantity_to_add)
                    updated_packages.append(updated_package)
                current_sector_packages.append(Package(product, quantity_to_add))
                first_sector_packs_num += 1
                sectors[0].add_to_sector(product, quantity_to_add)
            else:
                updated_packages.append(package)
        else:
            updated_packages.append(package)

    for position in sectors[0].positions:
        if len(current_sector_packages) == 0:
            break
        packages_to_insert = knapsack_shelf(storage, current_sector_packages, position)
        if position not in positions_actions.keys():
            positions_actions[position] = []
        for current_package in packages_to_insert:
            positions_actions[position].append(current_package)
            current_sector_packages.remove(current_package)

    container = Container(updated_packages)
    updated_packages = []
    for remain in current_sector_packages:
        container.add_package(remain)
    print("number of insertions in the first sector is ", first_sector_packs_num)
    # second stage + third stage:- check for top size_percentage products
    for i in range(1, 3):
        if not container.packages:
            break
        for package in container.packages:
            product = package.product
            total_quantity = package.quantity
            current_percent = sectors[i].get_percentage(product)
            max_percent = products_info[product.id].size_percentage
            max_add_quantity = int((max_percent - current_percent) * sectors[i].total_size)
            if current_percent < max_percent and max_add_quantity > 0:
                quantity_to_add = max_add_quantity
                if max_add_quantity >= total_quantity:
                    packages_to_remove.append(package)
                    quantity_to_add = total_quantity
                else:
                    updated_package = Package(product, total_quantity - quantity_to_add)
                    updated_packages.append(updated_package)
                current_sector_packages.append(Package(product, quantity_to_add))
                second_and_third_sector_packs_num += 1
                sectors[i].add_to_sector(product, quantity_to_add)
            else:
                updated_packages.append(package)

        for position in sectors[i].positions:
            packages_to_insert = knapsack_shelf(storage, current_sector_packages, position)
            if position not in positions_actions.keys():
                positions_actions[position] = []
            if len(current_sector_packages) == 0:
                break
            for current_package in packages_to_insert:
                positions_actions[position].append(current_package)
                current_sector_packages.remove(current_package)
        container = Container(updated_packages)
        updated_packages = []
        for remain in current_sector_packages:
            container.add_package(remain)
    print("second and third sectors insertions num is", second_and_third_sector_packs_num)
# fourth stage:- check for last_level products(knapsack)
    print("last sector insertions num is", len(container.packages))
    for package in container.packages:
        sectors[3].add_to_sector(package.product, package.quantity)

    for position in sectors[3].positions:
        if len(container.packages) == 0:
            break
        packages_to_insert = knapsack_shelf(storage, container.packages, position)
        if position not in positions_actions.keys():
            positions_actions[position] = []
        for current_package in packages_to_insert:
            positions_actions[position].append(current_package)
            container.remove_package(current_package)
    #print("last level are ready , supposed all your products quantity are in your storage")
    # fifth stage:- insert to the storage
    path = find_optimized_path(positions_actions.keys())
    for position in path:
        for package in positions_actions[position]:
            storage.insert_package(forklift, package, position)
    # last stage:- check if every product quantity are equal to the quantity you want
    """
    for row in storage.racks:
        for rack in row:
            for shelf in rack.shelves:
                for product in shelf.item_quantities.keys():
                    storage_quantity[product.id] += shelf.item_quantities[product]
    """
    # TODO: remove the code below' this is just for tests
    print("insertion completed successfully")
    storage_quantity = [0 for _ in range(100)]
    for row in storage_manager.storage.racks:
        for rack in row:
            for shelf in rack.shelves:
                for product in shelf.item_quantities.keys():
                    storage_quantity[product.id] += shelf.item_quantities[product]
    all_products_quantity = 0
    for i in range(len(storage_quantity)):
        # print("product ID=", i, "storage quantity=", storage_quantity[i])
        all_products_quantity += storage_quantity[i]
    print("printing quantity of all products in storage:-")
    print(all_products_quantity)
    """       
    # optimization settings
    priority_one_pos = build_territory([0], [0], range(0, storage.shelves_per_rack))
    priority_two_pos = build_territory(range(1, 3), range(1, 3), range(0, storage.shelves_per_rack))
    priority_three_pos = build_territory(range(3, 5), range(3, 5), range(0, storage.shelves_per_rack))
    percentaged_one_pos = build_territory(range(5, 7), range(5, 7), range(0, storage.shelves_per_rack))
    percentaged_two_pos = build_territory(range(7, 9), range(7, 9), range(0, storage.shelves_per_rack))
    free_area_pos = build_territory(range(9, storage.rows), range(9, storage.racks_per_row),
                                    range(0, storage.shelves_per_rack))

    # lists of packages according to where they should go
    # we should have info about current levels in storage
    priority_1 = []
    priority_2 = []
    priority_3 = []
    percentaged_1 = []
    percentaged_2 = []
    knapsacked = []
    for package in container.packages:
        info = storage_manager.items_info[package.product]
        # Is it prioritized?
        if info.frequency >= 0.1:
            priority_1.append(package)
        elif info.frequency >= 0.05:
            priority_2.append(package)
        elif info.frequency >= 0.025:
            priority_3.append(package)
        # TODO: make territory class and some info about items in it
        # TODO: for example: territory.item_info[product].quantitiy and/or a method territory.percentage(item)
        # Goes to percentaged section?
        #   percentaged_1.append(package) (if it allows saving proper percentages in percentaged level 1)
        #   percentaged_2.append(package) (if it allows saving proper percentages in percentaged level 2)
        # Knapsack them kids
        else:
            knapsacked.append(package)

    instructions_map = {}
    insert_instruction_knapsack(storage, priority_1, priority_one_pos, instructions_map)
    priority_2.extend(priority_1)  # TODO: check extreme cases
    insert_instruction_knapsack(storage, priority_2, priority_two_pos, instructions_map)
    priority_3.extend(priority_2)
    insert_instruction_knapsack(storage, priority_3, priority_three_pos, instructions_map)
    percentaged_1.extend(priority_3)
    insert_instruction_knapsack(storage, percentaged_1, percentaged_one_pos, instructions_map)
    percentaged_2.extend(percentaged_1)
    insert_instruction_knapsack(storage, percentaged_2, percentaged_two_pos, instructions_map)
    knapsacked.extend(percentaged_2)
    insert_instruction_knapsack(storage, knapsacked, free_area_pos, instructions_map)

    # Optimize path
    positions_on_path = instructions_map.keys()
    # path = optimize_path(positions_on_path)
    # for position in path:
    #   for package in instructions_map[position]:
    #       insert package to position
    """
    return


def insert_instruction_knapsack(storage, packages, positions, instructions_map):
    for position in positions:
        packages_in_pos = instructions_map[position] = knapsack_shelf(storage, packages, position)
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
        print("******************")
        print("storage quantity=", storage_quantity, "product ID=", product.id)
        print("needed quantity=", quantity)
        print("******************")
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
    print("extraction completed successfully")
    print("printing all quantities in our storage after the extraction")
    all_products_quantity = 0
    for i in range(len(storage_quantity)):
        # print("product ID=", i, "storage quantity=", storage_quantity[i])
        all_products_quantity += storage_quantity[i]
    print("printing quantity of all products in storage:-")
    print(all_products_quantity)


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
