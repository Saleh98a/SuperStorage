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
        product4 = Product(5, "fareed", 2, 2, "sa3eed")

        package1 = Package(product1, 10)
        package2 = Package(product2, 3)
        package3 = Package(product3, 3)
        package4 = Package(product3, 1)
        package5 = Package(product2, 3)
        package6 = Package(product1, 5)
        package7 = Package(product3, 5)
        package8 = Package(product2, 6)
        package9 = Package(product1, 3)

        print("printing the packages :- ")
        print("package 1 :- product is ", package1.product.name ,"quant is :-" , package1.quantity)
        print("package 2 :- product is ", package2.product.name, "quant is :-", package2.quantity)
        print("package 3 :- product is ", package3.product.name, "quant is :-", package3.quantity)
        print("package 4 :- product is ", package4.product.name, "quant is :-", package4.quantity)
        print("package 5 :- product is ", package5.product.name, "quant is :-", package5.quantity)
        print("package 6 :- product is ", package6.product.name, "quant is :-", package6.quantity)
        print("package 7 :- product is ", package7.product.name, "quant is :-", package7.quantity)
        print("package 8 :- product is ", package8.product.name, "quant is :-", package8.quantity)
        print("package 9 :- product is ", package9.product.name, "quant is :-", package9.quantity)
        cont1 = Container([])
        cont2 = Container([])
        cont3 = Container([])

        print("cont 1 before adding anything")
        i=0
        for package in cont1.packages:
            print("package number", i, ":-", package.product.name, package.quantity)
            i += 1
        cont1.add_package(package1)
        cont1.add_package(package2)
        cont1.add_package(package3)

        print("cont 1 after :-")
        i = 0
        for package in cont1.packages:
            print("package number", i, ":-", package.product.name, package.quantity)
            i += 1

        print("cont 2 before :-")
        i = 0
        for package in cont2.packages:
            print("package number", i, ":-", package.product.name, package.quantity)
            i += 1
        cont2.add_package(package4)
        cont2.add_package(package5)
        cont2.add_package(package6)
        print("cont 2 after :-")
        i = 0
        for package in cont2.packages:
            print("package number", i, ":-", package.product.name, package.quantity)
            i += 1

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
        ord1.add_to_order(product1, 19)
        ord1.add_to_order(product3, 5)
        storage_manager.extract_order(ord1)

        print("after extracting ord1")
        storage_manager.print()

        # ord2 = Order()
        # ord2.add_to_order(product3,5)
        # storage_manager.extract_order(ord2)

        print("after extracting ord2")
        storage_manager.print()

        print("*****************")
        print("inserting cont")
        cont_knapsack_test = Container()
        package10 = Package(product3, 2)
        package15 = Package(product4,1)
        package11 = Package(product3, 1)
        package12 = Package(product2, 1)
        package13 = Package(product2, 2)
        package14 = Package(product4, 1)
        cont_knapsack_test.add_package(package10)
        cont_knapsack_test.add_package(package15)
        cont_knapsack_test.add_package(package11)
        cont_knapsack_test.add_package(package12)
        cont_knapsack_test.add_package(package13)
        cont_knapsack_test.add_package(package14)
        storage_manager.insert_container(cont_knapsack_test)

        storage_manager.print()
        storage_manager.insert_container(cont1)
        storage_manager.insert_container(cont2)
        storage_manager.insert_container(cont3)


        storage_manager.print()