# coding: utf-8
"""This module is responsible for managing a provided database
by creating tables, inserting and querying data from it """

import offcleaner as cl
from offcleaner import ProductCleaner as pc
from mysql.connector import errorcode


class ProductRepository:

	def __init__(self, db, table_title="Product"):
		self.db = db
		self.table_title = "Product"
		self.headers = ["id", "name", "nutrition_grade", "url"]

	def create_prduct_table(self):
		"""This function is responsible for creating the product table"""

		cursor = self.db.cursor()

		table_description = (
			"CREATE TABLE Product ("
		    "id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,"
		    "name VARCHAR(150) NOT NULL,"
		    "nutrition_grade CHAR(1) NOT NULL,"
		    "url TEXT NOT NULL UNIQUE,"  # Preventing duplicates
		    "PRIMARY KEY (id)"
		)

		# Handling error block related to creating the table into the database
	    try:
	        print(f"Creating table {self.table_title}: ", end='')
	        cursor.execute(self.table_description)
	    except mysql.connector.Error as err:
	        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
	            print("already exists.")
	        else:
	            print(err.msg)
	    else:
	        print("OK")

		cursor.close()


	def insert_product_data(self):
		"""This function insert product data into an already created product table"""

		cursor = self.db.cursor()

		add_product = ("INSERT INTO Product "
              "(id, name, nutrition_grade, store, url) "
              "VALUES (%(id)s, %(name)s, %(nutrition_grade)s, %(url)s)")

		# Looping through each category and product to define each row

		# Loop through healthy and unhealthy food
		for parsed_data in (cl.pr.healthy_food_about, cl.pr.unhealthy_food_about):

			# Loop through each chosen category
			for category in cl.pr.api.category_list:

				# Loop through each product of the category while removing duplicates
				for barcode in (pc.extract_attribute_values_per_category(parsed_data, category, "code")):

					# Use offcleaner module to get list of attributes values per product
					product_row = pc.extract_attribute_list_per_product(parsed_data, category, barecode, "product_name", "nutrition_grades", 'url' )
				
					# Get a dictionary structure with zip
					data_product = dict(zip(self.headers, [None, *product_row]))

					# Create the row
					cursor.execute(add_product, data_product)


		self.db.commit()
		cursor.close()



	def get_product_data(self):
		pass
		# Do i need to write "USE Database" here ?












class CategoryRepository:

	def __init__(self,db):
		self.db = db
		self.table_title = "Category"
		self.headers = ["id", "name"]

	def create_category_table(self):
		"""This function is responsible for creating the category table"""

		cursor = self.db.cursor()

		table_description = (
			"CREATE TABLE Category ("
		    "id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,"
		    "name VARCHAR(150) NOT NULL UNIQUE,"             #Preventing duplicates
		    "PRIMARY KEY (id)"
		)

		# Creating the table and handling error related to creation
	    try:
	        print(f"Creating table {self.table_title}: ", end='')
	        cursor.execute(self.table_description)
	    except mysql.connector.Error as err:
	        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
	            print("already exists.")
	        else:
	            print(err.msg)
	    else:
	        print("OK")

		cursor.close()


	def insert_category_data(self):
		"""This function insert category data into an already created category table"""

		cursor = self.db.cursor()

		add_product = ("INSERT INTO Category "
              "(id, name) "
              "VALUES (%(id)s, %(name)s)")

		# Getting the complete list of categories
		# First, initilising with principal categories 
		complete_category_list = cl.pr.api.category_list

		# Loop through healthy and unhealthy food
		for parsed_data in (cl.pr.healthy_food_about, cl.pr.unhealthy_food_about):

			# Loop through each chosen principal category
			for category in cl.pr.api.category_list::

				# Flatten the list got from offcleaner module extract function
				nested_list= pc.extract_attribute_values_per_category(parsed_data, category, "categories_hierarchy")
				flatten_list = [subcategorie for subcategory_list in nested_list for subcategorie in subcategory_list ]

				# Joining sub categories from each principal category
				complete_category_list.extend(flatten_list)

		# Looping through each category and sub-category to define each row
		for category in complete_category_list :

			# One row content, initiliasing the id with None
			category_row = [None, category]

			# Get a dictionary structure with zip
			data_category = dict(zip(self.headers, category_row))

			# Create the row
			cursor.execute(add_product, data_category)


		self.db.commit()
		cursor.close()



	def get_category_data(self):
		pass
		# Do i need to write "USE Database" here ?


















class StoreRepository:
		def __init__(self,db):
		self.db = db
		self.table_title = "Store"
		self.headers = ["id", "name"]

	def create_store_table(self):
		"""This function is responsible for creating the store table"""

		cursor = self.db.cursor()

		table_description = (
			"CREATE TABLE Store ("
		    "id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,"
		    "name TEXT NOT NULL UNIQUE,"             #Preventing duplicates
		    "PRIMARY KEY (id)"
		)

		# Creating the table and handling error related to creation
	    try:
	        print(f"Creating table {self.table_title}: ", end='')
	        cursor.execute(self.table_description)
	    except mysql.connector.Error as err:
	        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
	            print("already exists.")
	        else:
	            print(err.msg)
	    else:
	        print("OK")

		cursor.close()



	def insert_store_data(self):
		"""This function insert store data into an already created store table"""

		cursor = self.db.cursor()

		add_product = ("INSERT INTO Store "
              "(id, name) "
              "VALUES (%(id)s, %(name)s)")

		# Looping through each category and product to define each row

		# Loop through healthy and unhealthy food
		for parsed_data in (cl.pr.healthy_food_about, cl.pr.unhealthy_food_about):

			# Loop through each chosen category
			for category in cl.pr.api.category_list:

				# Loop through each product of the category while removing duplicates 
				for barcode in list(set(pc.extract_attribute_values_per_category(parsed_data, category, "code"))):

					# Use offcleaner module to get list of attributes values per product
					product_row = pc.extract_attribute_list_per_product(parsed_data, category, barecode, "stores")
				
					# Get a dictionary structure with zip
					data_product = dict(zip(self.headers, [None, *product_row]))

					# Create the row
					cursor.execute(add_product, data_product)



		self.db.commit()
		cursor.close()




	def get_category_data(self):
		pass
		# Do i need to write "USE Database" here ?

class PCAssociationRepository:

class PSAssociationRepository:

class PPAssociationRepository:

class FavoriteRepository:































