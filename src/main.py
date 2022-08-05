from src.simulation.simulator import Simulator
from src.simulation.simulation_settings import SimulationSettings, InsertAlgorithm, ExtractAlgorithm
from src.storage.managers.storage_manager_settings import StorageManagerSettings
from src.storage.storages.storage_settings import StorageSettings


def main():
    simulator = Simulator(
        SimulationSettings(
            storage_managers_settings=[
                StorageManagerSettings(InsertAlgorithm.NAIVE, ExtractAlgorithm.OPTIMIZED),
                StorageManagerSettings(InsertAlgorithm.KNAPSACK, ExtractAlgorithm.OPTIMIZED),
                StorageManagerSettings(InsertAlgorithm.OPTIMIZED, ExtractAlgorithm.OPTIMIZED, [6, 15, 32]),
            ],
            storage_settings=StorageSettings(rows=20, racks_per_row=20, shelves_per_rack=10, shelf_size=200),
            operations_num=1000,
            insertion_headstart=15,
            extraction_probability=9/10,
            packages_per_container=30,
            products_per_order=10,
            insert_lambda_coeff=3,
            extract_lambda_coeff=2.5,
            repetitions_num=1,
            export=True,
        )
    )
    simulator.simulate()


if __name__ == '__main__':
    main()
