
import pandas as pd

from src.models.product import Product

def initialize_products():

    dataframe = pd.read_excel('src/simulation/products.xlsx')
    products = []

    for index, row in dataframe.iterrows():
        products.append(Product(row['id'],
                                row['product_name'],
                                row['weight'],
                                row['size'],
                                row['category_id'],
                                row['supplier_id']))

    return products
