# coding: utf-8
"""This module is responsible for defining the data to be manipulated """

from dbmanager import (ProductRepository, CategoryRepository)
from database import db

class Product:
	objects = ProductRepository(db)
	def __init__(
		self,
		name = None,
		barcode = None,
		store = None,
		url = None)
		self.id = None
		self.name = name
		self.barcode = barcode
		self.store = store
		self.url =url

class Category:
	objects = CategoryRepository(db)
	def __init__(
		self,
		name = None)
		self.id = None
		self.name = name
