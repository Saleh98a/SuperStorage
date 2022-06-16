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
        product1 = Product(1, "iPhone 7", 2, 3, "5ra")
        print("1")
        product2 = Product(4, "Tesla", 5, 6, "zbale")
        print("2")
        product3 = Product(7, "Galaxy s20", 8, 9, "za3eem")
        print("3")

        package1 = Package(product1, 10)
        print("4")
        package2 = Package(product2, 3)
        print("5")
        package3 = Package(product3, 4)
        package4 = Package(product3, 1)
        package5 = Package(product2, 9)
        package6 = Package(product1, 10)
        package7 = Package(product3, 5)
        package8 = Package(product2, 6)
        package9 = Package(product1, 7)
        print("6")
        cont1 = Container()
        print("7")
        cont2 = Container()
        print("8")
        cont3 = Container()
        cont1.add_package(package1)
        print("9")
        cont1.add_package(package2)
        print("10")
        cont1.add_package(package3)

        cont2.add_package(package4)
        cont2.add_package(package5)
        cont2.add_package(package6)
        print("11")
        cont3.add_package(package7)
        cont3.add_package(package8)
        print("12")
        cont3.add_package(package9)

        print("Inserting Containers")
        storage_manager.insert_container(cont1)
        print("13")
        storage_manager.insert_container(cont2)
        print("14")
        storage_manager.insert_container(cont3)

        print("success inserting, printing storage")

        storage_manager.print()
        ord1 = Order()
        ord1.add_to_order(product1, 10)
        storage_manager.extract_order(ord1)