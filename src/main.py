from src.simulation.simulator import Simulator
from src.simulation.simulation_settings import SimulationSettings, InsertAlgorithm, ExtractAlgorithm
from src.storage.managers.storage_manager_settings import StorageManagerSettings
from src.storage.storages.storage_settings import StorageSettings
import argparse

def main():
    parser = argparse.ArgumentParser(description='Super Storage Simulator')

    parser.add_argument("operations_num", help="The number of operations in this simulation")

    args = parser.parse_args()

    print(args.print_string)

    simulator = Simulator(
        SimulationSettings(
            storage_managers_settings=[
                StorageManagerSettings(InsertAlgorithm.NAIVE, ExtractAlgorithm.OPTIMIZED),
                StorageManagerSettings(InsertAlgorithm.KNAPSACK, ExtractAlgorithm.OPTIMIZED),
                StorageManagerSettings(InsertAlgorithm.OPTIMIZED, ExtractAlgorithm.OPTIMIZED, [6, 9, 32]),
            ],
            storage_settings=StorageSettings(rows=40, racks_per_row=40, shelves_per_rack=10, shelf_size=200),
            operations_num=1000,
            insertion_headstart=20,
            extraction_probability=8/10,
            packages_per_container=30,
            products_per_order=10,
            insert_lambda_coeff=3,
            extract_lambda_coeff=3,
            repetitions_num=1,
            export=True,
        )
    )
    simulator.simulate()


if __name__ == '__main__':
    main()
