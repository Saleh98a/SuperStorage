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
                    StorageManagerSettings(InsertAlgorithm.OPTIMIZED, ExtractAlgorithm.OPTIMIZED, [4, 8, 12]),
                ],
                storage_settings=StorageSettings(rows=25, racks_per_row=25, shelves_per_rack=10, shelf_size=200),
                operations_num=1500,
                insertion_headstart=15,
                extraction_probability=19/20,
                packages_per_container=30,
                products_per_order=10,
                insert_lambda_coeff=1,
                extract_lambda_coeff=0.8,
                repetitions_num=1,
                export=True,
            )
        ).simulate()
    except:
        print("failed")



if __name__ == '__main__':
    main()
