# coding: utf-8
"""This module is responsible for defining the data to be manipulated """

from dbmanager import (ProductRepository, CategoryRepository,
                       StoreRepository, CPAssociationRepository, PSAssociationRepository)
from database import db


class Product:
    objects = ProductRepository(db)

    def __init__(self, name=None, nutrition_grade=None, url=None):
        self.id = None
        self.name = name
        self.nutrition_grade = nutrition_grade
        self.url = url


class Category:
    objects = CategoryRepository(db)

    def __init__(self, name=None):
        self.id = None
        self.name = name


class Store:
    objects = StoreRepository(db)

    def __init__(self, name=None):
        self.id = None
        self.name = name


class CPAssociation:
    objects = CPAssociationRepository(db)

    def __init__(self):
        self.category_id = None
        self.product_id = None


class PSAssociation:
    objects = PSAssociationRepository(db)

    def __init__(self):
        self.store_id = None
        self.product_id = None


# Be sure not to execute creation and insertion more than once
#

def main():

    # Product.objects.create_product_table()
    # Product.objects.insert_product_data()
    # Category.objects.create_category_table()
    # Category.objects.insert_category_data()
    # Store.objects.create_store_table()
    # Store.objects.insert_store_data()
    # CPAssociation.objects.create_cpassociation_table()
    # CPAssociation.objects.insert_cpassociation_table()
    # PSAssociation.objects.create_psassociation_table()
    # PSAssociation.objects.insert_psassociation_table()


if __name__ == "__main__":
    main()
