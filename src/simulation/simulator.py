"""
Simulator Class
Runs a storage environment simulation
"""
from src.models.container import Container
from src.models.order import Order
from src.models.package import Package
from src.models.product import Product


class Simulator:

    @staticmethod
    def simulate(storage_manager):#, simulation_settings):
        # TODO: Temporary Implementation
        product1 = Product(1, "iPhone 7", 2, 3, "5ra")
        product2 = Product(4, "Tesla", 5, 6, "zbale")
        product3 = Product(7, "Galaxy s20", 8, 9, "za3eem")

        package1 = Package(product1, 10)
        package2 = Package(product2, 3)
        package3 = Package(product3, 4)
        package4 = Package(product3, 1)
        package5 = Package(product2, 3)
        package6 = Package(product1, 5)
        package7 = Package(product3, 5)
        package8 = Package(product2, 6)
        package9 = Package(product1, 3)
        cont1 = Container()
        cont2 = Container()
        cont3 = Container()
        cont1.add_package(package1)
        cont1.add_package(package2)
        cont1.add_package(package3)

        cont2.add_package(package4)
        cont2.add_package(package5)
        cont2.add_package(package6)

        cont3.add_package(package7)
        cont3.add_package(package8)
        cont3.add_package(package9)

        print("Inserting Containers")
        storage_manager.insert_container(cont1)
        storage_manager.insert_container(cont2)
        storage_manager.insert_container(cont3)

        print("Inserting Succeeded.. Printing storage")

        storage_manager.print()
        ord1 = Order()
        ord1.add_to_order(product1, 10)
        storage_manager.extract_order(ord1)