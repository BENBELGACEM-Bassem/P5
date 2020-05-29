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
            "barcode BIGINT NOT NULL UNIQUE,"
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
                cl.pr.HEALTHY_DATA_LOCAL_COPY,
                cl.pr.UNHEALTHY_DATA_LOCAL_COPY):
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
                    data_product = dict(
                        zip(self.headers, [None, *product_row]))
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
        complete_category_list = pc.all_categories_involved(
            cl.pr.HEALTHY_DATA_LOCAL_COPY, cl.pr.UNHEALTHY_DATA_LOCAL_COPY)
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

        for store in pc.all_stores_involved(cl.pr.HEALTHY_DATA_LOCAL_COPY, cl.pr.UNHEALTHY_DATA_LOCAL_COPY):

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

        # Choosing the option giving dictionary as output
        cursor = self.db.cursor(dictionary=True, buffered=True)

        add_product = ("INSERT INTO CPAssociation "
                       "(category_id, product_id) "
                       "VALUES (%(category_id)s, %(product_id)s)"
                       "ON DUPLICATE KEY UPDATE product_id = product_id")

        for parsed_data in (
                cl.pr.HEALTHY_DATA_LOCAL_COPY,
                cl.pr.UNHEALTHY_DATA_LOCAL_COPY):

            for category in cl.pr.api.category_list:
                query = ("SELECT id FROM Category "
                         "WHERE name = %s")
                cursor.execute(query, (category,))
                principal_category_id = [row['id'] for row in cursor]

                product_list = pc.extract_attribute_values_per_category(
                    parsed_data, category, "code")

                for barcode in product_list:

                    query = ("SELECT id FROM Product "
                             "WHERE barcode = %s")
                    cursor.execute(query, (barcode,))
                    product_id = [row['id'] for row in cursor][0]

                    subcategories_list = sum(pc.extract_attribute_list_per_product(
                        parsed_data, category, barcode, "categories_hierarchy"), [])
                    query = (f"""SELECT id FROM Category
	                         WHERE name IN ({','.join('%s' for _ in subcategories_list)})""")
                    cursor.execute(query, tuple(subcategories_list))
                    subcategories_id_list = [row['id'] for row in cursor]

                    category_id_list = list(
                        set(subcategories_id_list + principal_category_id))

                    for category_id in category_id_list:
                        data_product = dict(
                            zip(self.headers, [category_id, product_id]))
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
            "CONSTRAINT fk_food_id FOREIGN KEY (product_id) REFERENCES Product(id),"
            "CONSTRAINT fk_store_id FOREIGN KEY (store_id) REFERENCES Store(id),"
            "PRIMARY KEY (product_id, store_id))"      # composite primary key
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

        add_product = ("INSERT INTO PSAssociation "
                       "(product_id, store_id) "
                       "VALUES (%(product_id)s, %(store_id)s)"
                       "ON DUPLICATE KEY UPDATE product_id = product_id")

        # Loop through healthy and unhealthy food
        for parsed_data in (
                cl.pr.HEALTHY_DATA_LOCAL_COPY,
                cl.pr.UNHEALTHY_DATA_LOCAL_COPY):

            for category in cl.pr.api.category_list:

                product_list = pc.extract_attribute_values_per_category(
                    parsed_data, category, "code")

                for barcode in product_list:
                    query = ("SELECT id FROM Product "
                             "WHERE barcode = %s")
                    cursor.execute(query, (barcode,))
                    product_id = [row['id'] for row in cursor][0]

                    stores_list = pc.all_stores_involved_per_product(
                        parsed_data, category, barcode)

                    stores_id_list = []

                    for name in stores_list:
                        query = ("SELECT id FROM Store "
                                 "WHERE name = %s")
                        cursor.execute(query, (name,))
                        store_id = [row['id'] for row in cursor][0]
                        stores_id_list.append(store_id)

                    for store_id in stores_id_list:
                        data_product = dict(
                            zip(self.headers, [product_id, store_id]))
                        cursor.execute(add_product, data_product)

        self.db.commit()
        cursor.close()


class PPAssociationRepository:
    pass


class FavoriteRepository:
    pass
