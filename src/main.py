from src.simulation.simulator import Simulator
from src.simulation.simulation_settings import SimulationSettings, InsertAlgorithm, ExtractAlgorithm
from src.storage.managers.storage_manager_settings import StorageManagerSettings
from src.storage.storages.storage_settings import StorageSettings

def main():

    try:
        Simulator(
            SimulationSettings(
                storage_managers_settings=[
                    StorageManagerSettings(InsertAlgorithm.NAIVE, ExtractAlgorithm.OPTIMIZED),
                    StorageManagerSettings(InsertAlgorithm.KNAPSACK, ExtractAlgorithm.OPTIMIZED),
                    StorageManagerSettings(InsertAlgorithm.OPTIMIZED, ExtractAlgorithm.OPTIMIZED, [5, 9, 13]),
                ],
                storage_settings=StorageSettings(rows=40, racks_per_row=40, shelves_per_rack=10, shelf_size=200),
                operations_num=3000,
                insertion_headstart=15,
                extraction_probability=3/10,
                packages_per_container=30,
                products_per_order=10,
                insert_lambda_coeff=5,
                extract_lambda_coeff=3,
                repetitions_num=1,
                export=True,
            )
        ).simulate()
    except:
        print("failed")

    try:
        Simulator(
            SimulationSettings(
                storage_managers_settings=[
                    StorageManagerSettings(InsertAlgorithm.NAIVE, ExtractAlgorithm.OPTIMIZED),
                    StorageManagerSettings(InsertAlgorithm.KNAPSACK, ExtractAlgorithm.OPTIMIZED),
                    StorageManagerSettings(InsertAlgorithm.OPTIMIZED, ExtractAlgorithm.OPTIMIZED, [5, 9, 13]),
                ],
                storage_settings=StorageSettings(rows=40, racks_per_row=40, shelves_per_rack=10, shelf_size=200),
                operations_num=3000,
                insertion_headstart=15,
                extraction_probability=4/10,
                packages_per_container=30,
                products_per_order=10,
                insert_lambda_coeff=5,
                extract_lambda_coeff=3,
                repetitions_num=1,
                export=True,
            )
        ).simulate()
    except:
        print("failed")



if __name__ == '__main__':
    main()
