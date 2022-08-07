from src.simulation.simulator import Simulator
from src.simulation.simulation_settings import SimulationSettings, InsertAlgorithm, ExtractAlgorithm
from src.storage.managers.storage_manager_settings import StorageManagerSettings
from src.storage.storages.storage_settings import StorageSettings
import argparse

def simulation_script():
    parser = argparse.ArgumentParser(description='Super Storage Simulator')

    parser.add_argument("--ss_rows", help="Number of row in our SuperStorage", required=False, default=40)
    parser.add_argument("--ss_racks_per_row", help="Number of racks per row in our SuperStorage", required=False, default=40)
    parser.add_argument("--ss_shelves_per_rack", help="Number of shelves per rack in our SuperStorage", required=False, default=10)
    parser.add_argument("--ss_shelf_size", help="Size of shelves in our SuperStorage", required=False, default=200)

    parser.add_argument("--operations_num", help="Number of operations in this simulation", required=False, default=1000)
    parser.add_argument("--insertion_headstart", help="Number of insertions at the start of the simulation", required=False, default=20)
    parser.add_argument("--extraction_probability", help="The probability of drawing extraction operations", required=False, default=8/10)
    parser.add_argument("--exponential_scale", help="Equal to 1/λ (λ is the parameter of exponential distribution)", required=False, default=20)
    parser.add_argument("--packages_per_container", help="Packages per one inserted container", required=False, default=30)
    parser.add_argument("--products_per_order", help="Products per one extraction order", required=False, default=10)
    parser.add_argument("--insert_lambda_coeff", help="Coefficient for the insertion Poisson parameter", required=False, default=3)
    parser.add_argument("--extract_lambda_coeff", help="Coefficient for the extraction Poisson parameter", required=False, default=3)
    parser.add_argument("--sector_bounds", help="Sector Bounds for Optimized Algorithm", required=False, default=[6, 9, 32])
    parser.add_argument("--export", help="Export results to files", required=False, default=True)

    parser.add_argument("--storage_managers", "--sm",
                        help="""Adds a Storage Manager to run: --sm insert_algo, extract_algo, ...sector_bounds?
                                Examples: 
                                --sm knapsack, optimized
                                --sm optimized, optimized, 6, 9, 32
                                in the latter case 6, 9, 32 are the sector bounds""",
                        action="append",
                        nargs='+',
                        required=False,
                        default=None)

    args = parser.parse_args()

    if args.storage_managers == None:
        args.storage_managers = [["naive", "optimized"], ["knapsack", "optimized"], ["optimized", "optimized", 6, 9, 32]]

    print(args.storage_managers)

    storage_managers = [
        StorageManagerSettings(InsertAlgorithm.from_string(storage_manager[0]), ExtractAlgorithm.from_string(storage_manager[1]), sector_bounds=list(map(int, storage_manager[2:])) if 2 < len(storage_manager) else None)
        for storage_manager in args.storage_managers
    ]

    simulator = Simulator(
        SimulationSettings(
            storage_managers_settings=storage_managers,
            storage_settings=StorageSettings(
                rows=args.ss_rows,
                racks_per_row=args.ss_racks_per_row,
                shelves_per_rack=args.ss_shelves_per_rack,
                shelf_size=args.ss_shelf_size),
            operations_num=args.operations_num,
            insertion_headstart=args.insertion_headstart,
            exponential_scale=args.exponential_scale,
            extraction_probability=args.extraction_probability,
            packages_per_container=args.packages_per_container,
            products_per_order=args.products_per_order,
            insert_lambda_coeff=args.insert_lambda_coeff,
            extract_lambda_coeff=args.extract_lambda_coeff,
            repetitions_num=1,
            export=args.export,
        )
    )
    simulator.simulate()

    input("press any key to exit")

if __name__ == '__main__':
    simulation_script()
