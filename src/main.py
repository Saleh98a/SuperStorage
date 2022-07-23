from src.simulation.simulator import Simulator
from src.simulation.simulation_settings import SimulationSettings, InsertAlgorithm, ExtractAlgorithm
from src.storage.managers.storage_manager_settings import StorageManagerSettings


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
        SimulationSettings(storage_managers_settings=[
                                StorageManagerSettings(InsertAlgorithm.NAIVE, ExtractAlgorithm.OPTIMIZED),
                                StorageManagerSettings(InsertAlgorithm.KNAPSACK, ExtractAlgorithm.OPTIMIZED),
                                StorageManagerSettings(InsertAlgorithm.OPTIMIZED, ExtractAlgorithm.OPTIMIZED, [6, 14, 32]),
                            ],
                           operations_num=600,
                           extraction_probability=19/20,
                           packages_per_container=40,
                           products_per_order=5,
                           insertion_headstart=8,
                           repetitions_num=1))
    sim2.simulate()


if __name__ == '__main__':
    my_main()
