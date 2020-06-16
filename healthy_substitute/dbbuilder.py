"""This module is responsible for building the user database"""

import models

from models import Product, Category, Store


def main():
    """Build the content of the data base"""
    Product.objects.create_product_table()
    Product.objects.insert_product_data()
    Category.objects.create_category_table()
    Category.objects.insert_category_data()
    Store.objects.create_store_table()
    Store.objects.insert_store_data()
    models.dbmanager.CPAssociationRepository(
        models.db).create_cpassociation_table()
    models.dbmanager.CPAssociationRepository(
        models.db).insert_cpassociation_table()
    models.dbmanager.PSAssociationRepository(
        models.db).create_psassociation_table()
    models.dbmanager.PSAssociationRepository(
        models.db).insert_psassociation_table()
    Product.objects.create_favourite_table()

if __name__ == "__main__":
    main()
