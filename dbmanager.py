# coding: utf-8
"""This module is responsible for managing a provided database
by creating tables, inserting and querying data from it """

import offcleaner as cl
from offcleaner import ProductCleaner as pc
from decorators import run_once
import mysql.connector
from mysql.connector import errorcode

class ProductRepository:

    def __init__(self, db, table_title="Product"):
        self.db = db
        self.table_title = "Product"
        self.headers = ["id", "barcode", "name", "nutrition_grade", "url"]

    @run_once
    def create_product_table(self):
        """This function is responsible for creating the product table"""

        cursor = self.db.cursor()

        table_description = (
            "CREATE TABLE Product ("
            "id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,"
            "barcode BIGINT NOT NULL UNIQUE,"               # Preventing duplicates
            "name VARCHAR(255),"
            "nutrition_grade CHAR(1) NOT NULL,"
            "url TEXT NOT NULL,"
            "PRIMARY KEY (id))"
        )

        # Handling error block related to creating the table into the database
        try:
            print(f"Creating table {self.table_title}: ", end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        cursor.close()

    @run_once
    def insert_product_data(self):
        """This function insert product data into an already created product table"""

        cursor = self.db.cursor()

        add_product = (
            "INSERT INTO Product "
            "(id, barcode, name, nutrition_grade, url)"
            "VALUES (%(id)s, %(barcode)s, %(name)s, %(nutrition_grade)s, %(url)s)"
            "ON DUPLICATE KEY UPDATE id = id")

        # Looping through each category and product to define each row

        # Loop through healthy and unhealthy food
        for parsed_data in (
                cl.pr.healthy_food_about,
                cl.pr.unhealthy_food_about):

            # Loop through each chosen category
            for category in cl.pr.api.category_list:

                # Loop through each product of the category while removing
                # duplicates

                for barcode in (
                    pc.extract_attribute_values_per_category(
                        parsed_data, category, "code")):

                    # Use offcleaner module to get list of attributes values
                    # per product
                    product_row = pc.extract_attribute_list_per_product(
                        parsed_data, category, barcode, "code", "product_name", "nutrition_grades", 'url')

                    # Get a dictionary structure with zip
                    data_product = dict(zip(self.headers, [None, *product_row]))

                    # Create the row
                    cursor.execute(add_product, data_product)


        self.db.commit()
        cursor.close()

    # Do i need to write "USE Database" hereafter ?

    def get_by_category(self, category):
        pass

    def get_substitute_for_product(self, product):
        pass

    def save(self, product):
        pass


class CategoryRepository:

    def __init__(self, db):
        self.db = db
        self.table_title = "Category"
        self.headers = ["id", "name"]

    @run_once
    def create_category_table(self):
        """This function is responsible for creating the category table"""

        cursor = self.db.cursor()

        table_description = (
            "CREATE TABLE Category ("
            "id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,"
            "name VARCHAR(255) NOT NULL UNIQUE,"  # Preventing duplicates
            "PRIMARY KEY (id))"
        )

        # Handling error block related to creating the table into the database
        try:
            print(f"Creating table {self.table_title}: ", end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        cursor.close()

    @run_once
    def insert_category_data(self):
        """This function insert category data into an already created category table"""

        cursor = self.db.cursor()

        add_product = ("INSERT INTO Category "
                       "(id, name) "
                       "VALUES (%(id)s, %(name)s)"
                       "ON DUPLICATE KEY UPDATE id = id")


        complete_category_list = pc.all_categories_involved(cl.pr.healthy_food_about, cl.pr.unhealthy_food_about)

        # Looping through each category and sub-category to define each row
        for category in complete_category_list:

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

    def __init__(self, db):
        self.db = db
        self.table_title = "Store"
        self.headers = ["id", "name"]

    @run_once
    def create_store_table(self):
        """This function is responsible for creating the store table"""

        cursor = self.db.cursor()

        table_description = (
            "CREATE TABLE Store ("
            "id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,"
            "name VARCHAR(255) NOT NULL UNIQUE,"  # Preventing duplicates
            "PRIMARY KEY (id))"
        )

        # Handling error block related to creating the table into the database
        try:
            print(f"Creating table {self.table_title}: ", end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        cursor.close()

    @run_once
    def insert_store_data(self):
        """This function insert store data into an already created store table"""

        cursor = self.db.cursor()

        add_product = ("INSERT INTO Store "
                       "(id, name) "
                       "VALUES (%(id)s, %(name)s)"
                       "ON DUPLICATE KEY UPDATE id = id")

        # Looping through each product to define each row

        for store in pc.all_stores_involved(cl.pr.healthy_food_about, cl.pr.unhealthy_food_about):

            # Get a dictionary structure with zip
            data_product = dict(
                zip(self.headers, [None, store]))

            # Create the row
            cursor.execute(add_product, data_product)

        self.db.commit()
        cursor.close()









class CPAssociationRepository:

    def __init__(self, db, table_title="CPAssociation"):
        self.db = db
        self.table_title = "CPAssociation"
        self.headers = ["category_id", "product_id"]

    @run_once
    def create_cpassociation_table(self):
        """This function is responsible for creating the category_product association table"""

        cursor = self.db.cursor()

        table_description = (
            "CREATE TABLE CPAssociation ("
            "category_id SMALLINT UNSIGNED NOT NULL,"
            "product_id SMALLINT UNSIGNED NOT NULL,"
            "CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES Category(id),"
            "CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES Product(id),"
            "PRIMARY KEY (category_id, product_id))"
        )

        # Handling error block related to creating the table into the database
        try:
            print(f"Creating table {self.table_title}: ", end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        cursor.close()


    @run_once
    def insert_cpassociation_table(self):
        """This function insert data into an already created category_product association table"""

        #Choosing the option giving dictionary as output
        cursor = self.db.cursor(dictionary=True, buffered=True)

        add_product = ("INSERT INTO CPAssociation "
                       "(category_id, product_id) "
                       "VALUES (%(category_id)s, %(product_id)s)")


        for parsed_data in (
                cl.pr.healthy_food_about,
                cl.pr.unhealthy_food_about):

        	#Loop through principal categories
	        for category in cl.pr.api.category_list:
	            query = ("SELECT id FROM Category "
	                     "WHERE name = %s")
	            cursor.execute(query, (category,))
	            category_id = [row['id'] for row in cursor][0]

	            #Find all product id related to that category
	            product_list = pc.extract_attribute_values_per_category(
                    parsed_data, category, "code")
	            query = (f"""SELECT id FROM Product 
                         WHERE barcode IN ({','.join('%s' for _ in product_list)})""")
	            cursor.execute(query, tuple(product_list))
	            product_id_list = [row['id'] for row in cursor]

	            #Find all subcategories id
	            for barcode in product_list:
	            	subcategories_list = sum(pc.extract_attribute_list_per_product(
                        parsed_data, category, barcode, "categories_hierarchy"),[])

	            	query = (f"""SELECT id FROM Category
                             WHERE name IN ({','.join('%s' for _ in subcategories_list)})""")
	            	cursor.execute(query, tuple(subcategories_list))
	            	subcategories_id_list = [row['id'] for row in cursor]

            	#Filling the association table, first for principal category, then for subcategories
	            for product_id in product_id_list:
            		data_product = dict(zip(self.headers, [category_id, product_id]))
            		cursor.execute(add_product, data_product)

            		for subcategory_id in subcategories_id_list:
            			data_product = dict(zip(self.headers, [subcategory_id, product_id]))
            			cursor.execute(add_product, data_product)


        self.db.commit()
        cursor.close()


class PSAssociationRepository:

    def __init__(self, db, table_title="PSAssociation"):
        self.db = db
        self.table_title = "PSAssociation"
        self.headers = ["product_id", "store_id"]

    @run_once
    def create_psassociation_table(self):
        """This function is responsible for creating the product_store association table"""

        cursor = self.db.cursor()

        table_description = (
            "CREATE TABLE PSAssociation ("
            "product_id SMALLINT UNSIGNED NOT NULL,"
            "store_id SMALLINT UNSIGNED NOT NULL,"
            "CONSTRAINT fk_product_id"
            "FOREIGN KEY (product_id)"
            "REFERENCES Product(id),"
            "CONSTRAINT fk_store_id"
            "FOREIGN KEY (store_id)"
            "REFERENCES Store(id),"
            "PRIMARY KEY (product_id, store_id)"      # composite primary key
        )

        # Handling error block related to creating the table into the database
        try:
            print(f"Creating table {self.table_title}: ", end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        cursor.close()

    @run_once
    def insert_psassociation_table(self):
        """This function insert data into an already created category_product association table"""

        cursor = self.db.cursor(dictionary=True, buffered=True)

        # Loop through healthy and unhealthy food
        for parsed_data in (
                cl.pr.healthy_food_about,
                cl.pr.unhealthy_food_about):

            # Looping through all parsed products
            product_url_list = pc.extract_attribute_values_per_category(
                parsed_data, category, "url")
            for product_url in product_url_list:

                # Select product id from Product table based on the product url
                query = ("SELECT id FROM Product "
                         "WHERE url = product_url")

                cursor.execute(query)

                product_id = [row['id'] for row in cursor][0]

                # Get the barcode of this product from the url
                barcode = product_url.split('/')[4]

                # Get stores related to this product
                stores_list = pc.extract_attribute_list_per_product(
                    parsed_data, category, barecode, "stores")[0].split(",")

                # Replacing absent store name by a customized message in
                # accordance with the Store table
                stores_cleaned_list = [
                    i if (i and i != '') else "Unknown shopping place" for i in stores_list]

                # Getting all the stores id
                query = ("SELECT id FROM Store "
                         "WHERE name in stores_cleaned_list")

                cursor.execute(query)

                store_id_list = [row['id'] for row in cursor]

                # Loop through found store id list, then insert into the
                # association table
                for store_id in store_id_list:

                    # Get a dictionary structure with zip
                    data_product = dict(
                        zip(self.headers, [product_id, store_id]))
                    # Create the row
                    cursor.execute(add_product, data_product)

        self.db.commit()
        cursor.close()


class PPAssociationRepository:
    pass


class FavoriteRepository:
    pass

