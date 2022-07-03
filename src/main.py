# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from random import randint
import numpy as np
# from scipy.stats import norm
# import scipy as scipy

from simulation.simulator import Simulator

from src.simulation.simulation_settings import SimulationSettings, InsertAlgorithm, ExtractAlgorithm


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sim2 = Simulator(SimulationSettings(insert_algo=InsertAlgorithm.KNAPSACK,
                                        extract_algo=ExtractAlgorithm.NAIVE))
    sim2.simulate()
    """
    print("starting to learn our distribution :-")
    # size[i]/total_size
    # product_quantity_mean/all_quantities (This isn't what we want)
    # => size[i]*product_quantity_mean / sigma_quantity (size[j])
    # Each product quantity is poisson distribution with quantities_lambda[i] parameter for product i
    products_num = 10
    quantities_lambda = [randint(1, 5) for _ in
                         range(products_num)]  # the lambda of every product quantity distribution
    # mu and sigma are the parameters for normal distribution
    mu = randint(3, 7)
    sigma = randint(1, 3)
    sample_size = 1000000
    # sample of products num that distributed with normal distribution  with sigma and mu parameters
    # possible_orders_product = np.random.normal(mu, sigma, sample_size)
    possible_orders_product = [randint(0, products_num - 1) for _ in range(sample_size)]
    possible_orders_quantity = []
    total_quantity = 0
    total_products_quantity = [0 for i in range(products_num)]
    total_products_orders = [0 for i in range(products_num)]
    for i in range(sample_size):
        while possible_orders_product[i] < 0 or possible_orders_product[i] > products_num:
            possible_orders_product[i] = np.random.normal(mu, sigma, 1)[0]
        possible_orders_product[i] = int(possible_orders_product[i])
        lamda = quantities_lambda[int(possible_orders_product[i])]
        quantity = int(np.random.poisson(lamda, 1)[0])
        possible_orders_quantity.append(quantity)
        total_products_orders[int(possible_orders_product[i])] += 1
        total_products_quantity[int(possible_orders_product[i])] += quantity
        total_quantity += quantity
    total_error = 0
    for i in range(products_num):
        theoretical_product_distribution = 1 / products_num
        theoretical_product_quantity = quantities_lambda[i]
        theoretical_frequency = theoretical_product_quantity * theoretical_product_distribution
        # measured = (total_products_orders[i]/sample_size) * (total_products_quantity[i]/total_products_orders[i])
        measured = 0
        if total_products_quantity[i]:
            measured = (total_products_orders[i] / sample_size) * (total_products_quantity[i] / total_products_orders[i])
            measured = (total_products_quantity[i] / total_quantity)
        print("the true frequency of product", i + 1, "is ", theoretical_frequency, "measured frequency is ", measured)
        total_error += abs(measured - theoretical_frequency) / theoretical_frequency
    print("total error is :- ", total_error / products_num)
            measured = (total_products_orders[i]/sample_size) * (total_products_quantity[i]/total_products_orders[i])
            measured = (total_products_quantity[i]/total_quantity)
        print("the true frequency of product", i+1, "is ", theoretical_frequency, "measured frequency is ", measured)
        total_error += abs(measured - theoretical_frequency)/theoretical_frequency
    print("total error is :- ", total_error/products_num)
    """
    """
    s2 = SuperStorage()
    knapsack1 = KnapsackStorageManager(s2)
    sim2 = Simulator()
    sim2.simulate(knapsack1)
    """
    print_hi('It\'s Chewsday Innit')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# def learn(products) => updates the frequency/percentage/....
