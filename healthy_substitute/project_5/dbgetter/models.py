"""This module is responsible for defining the data to be manipulated"""

from . import dbmanager

from ..userdb import db


class Product:
    """This class defines the object product"""

    objects = dbmanager.ProductRepository(db)

    def __init__(
            self,
            barcode,
            name=None,
            nutrition_grade=None,
            url=None,
            id=None):
        """Initialise products attributes"""
        self.id = id
        self.barcode = barcode
        self.name = name
        self.nutrition_grade = nutrition_grade
        self.url = url

    def __str__(self):
        """Define how a product is printed"""
        return (
            f"barcode:{self.barcode}, name:{self.name}," +
            f"nutrition_grade:{self.nutrition_grade}, url:{self.url}")

    def __repr__(self):
        """Define how a product is presented with necessary attributes"""
        return (
            f"barcode:{self.barcode}, name:{self.name}," +
            f"nutrition_grade:{self.nutrition_grade}")


class Category:
    """This class defines the object category"""

    objects = dbmanager.CategoryRepository(db)

    def __init__(self, category_id, name=None):
        """Initialise category attributes"""
        self.id = category_id
        self.name = name

    def __str__(self):
        """Define how a category is printed"""
        return f"id:{self.id}, name:{self.name}"


class Store:
    """This class defines the object product"""

    objects = dbmanager.StoreRepository(db)

    def __init__(self, name):
        """Initialise store attributes"""
        self.id = None
        self.name = name

    def __str__(self):
        """Define how a store is printed"""
        return f"store:{self.name}"
