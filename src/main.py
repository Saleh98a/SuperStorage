from src.simulation.simulator import Simulator
from src.simulation.simulation_settings import SimulationSettings, InsertAlgorithm, ExtractAlgorithm


def my_main():
    """
    products = initialize_products()
    learned_info = learn(products, 100000)
    store = SuperStorage()
    bounds = [2, 8, 14]
    manager = StorageManager(store, InsertAlgorithm.OPTIMIZED, ExtractAlgorithm.OPTIMIZED, bounds, learned_info)
    for i in range(10):
        first_container = Container()
        second_container = Container()
        third_container = Container()
        first_order = Order()
        second_order = Order()
        for product in products:
            first_container.add_package(Package(product, 3))
            second_container.add_package(Package(product, 5))
            third_container.add_package(Package(product, 2))
            first_order.add_to_order(product, 5)
            second_order.add_to_order(product, 5)
        manager.insert_container(first_container)
        manager.insert_container(second_container)
        manager.extract_order(first_order)
        if i % 2:
            manager.extract_order(second_order)
        manager.insert_container(third_container)
    """
    sim2 = Simulator(
        SimulationSettings(insert_algo=[InsertAlgorithm.NAIVE, InsertAlgorithm.KNAPSACK, InsertAlgorithm.OPTIMIZED],
                           extract_algo=[ExtractAlgorithm.NAIVE, ExtractAlgorithm.OPTIMIZED],
                           containers_num=20,
                           repetitions_num=10))
    sim2.simulate()


if __name__ == '__main__':
    my_main()
