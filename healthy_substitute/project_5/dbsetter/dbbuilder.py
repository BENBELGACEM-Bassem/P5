"""This module is responsible for building the user database"""

import mysql.connector

from mysql.connector import errorcode

from ..userdb import db

from .offcleaner import ProductCleaner as pcl

from .configuration import ApiOff as api


class ProductBuilder:
    """This class manages product data insertion into a given database"""

    def __init__(self, db):
        """Initialise product table instance"""
        self.db = db
        self.headers = ["id", "barcode", "name", "nutrition_grade", "url"]

    def create_product_table(self):
        """Create the product table"""
        cursor = self.db.cursor()
        table_description = (
            """CREATE TABLE Product (
            id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
            barcode BIGINT NOT NULL UNIQUE,
            name VARCHAR(255),
            nutrition_grade CHAR(1) NOT NULL,
            url TEXT NOT NULL,
            PRIMARY KEY (id))""")
        try:
            print("Creating table Product: ")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
        cursor.close()

    def create_favourite_table(self):
        """Create the favourite product table"""
        cursor = self.db.cursor()
        table_description = (
            """CREATE TABLE Favourite_product (
            id SMALLINT UNSIGNED NOT NULL,
            CONSTRAINT fk_favourite_id
            FOREIGN KEY (id)
            REFERENCES Product(id))""")
        try:
            print("Creating table Favourite_product: ")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        cursor.close()

    def insert_product_data(self, product_rows):
        """Insert product data into an already created product table"""
        cursor = self.db.cursor()
        add_product = (
            """INSERT INTO Product
            (id, barcode, name, nutrition_grade, url)
            VALUES (%(id)s,
            %(barcode)s,
            %(name)s,
            %(nutrition_grade)s,
            %(url)s)
            ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id)""")

        rows = product_rows
        for row in rows:
            data_product = dict(
                zip(self.headers, [None, *row]))
            cursor.execute(add_product, data_product)
        self.db.commit()
        cursor.close()


class CategoryBuilder:
    """This class manages product data insertion into a given database"""

    def __init__(self, db):
        """Initialise category table instances"""
        self.db = db
        self.headers = ["id", "name"]

    def create_category_table(self):
        """Create the category table"""
        cursor = self.db.cursor()
        table_description = (
            """CREATE TABLE Category (
            id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL UNIQUE,
            PRIMARY KEY (id))""")
        try:
            print("Creating table Category: ")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        cursor.close()

    def insert_category_data(self, categories):
        """Insert category data into an already created category table"""
        cursor = self.db.cursor()
        add_product = ("""INSERT INTO Category
                       (id, name)
                       VALUES (%(id)s, %(name)s)
                       ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id)""")
        # All categories involved
        complete_category_list = list(set(sum(categories.values(), [])))
        for category in complete_category_list:
            category_row = [None, category]
            data_category = dict(zip(self.headers, category_row))
            cursor.execute(add_product, data_category)
        self.db.commit()
        cursor.close()


class StoreBuilder:
    """Manage the database with regard to the store object"""

    def __init__(self, db):
        """Initialise store table instances"""
        self.db = db
        self.headers = ["id", "name"]

    def create_store_table(self):
        """Create the store table"""
        cursor = self.db.cursor()
        table_description = (
            """CREATE TABLE Store (
            id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL UNIQUE,
            PRIMARY KEY (id))""")
        try:
            print("Creating table Store: ")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
        cursor.close()

    def insert_store_data(self, stores):
        """Insert store data into an already created table"""
        cursor = self.db.cursor()
        add_product = ("""INSERT INTO Store
                       (id, name)
                       VALUES (%(id)s, %(name)s)
                       ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id)""")
        # All stores involved
        complete_store_list = list(set(sum(stores.values(), [])))
        for store in complete_store_list:
            data_product = dict(
                zip(self.headers, [None, store]))
            cursor.execute(add_product, data_product)
        self.db.commit()
        cursor.close()


class CPassociationBuilder:
    """This class manages the database

    with regard to the category-product association object
    """

    def __init__(self, db):
        """Initialise product_category table instances"""
        self.db = db
        self.headers = ["category_id", "product_id"]

    def create_cpassociation_table(self):
        """Create the category_product association table"""
        cursor = self.db.cursor()
        table_description = (
            """CREATE TABLE CPAssociation (
            category_id SMALLINT UNSIGNED NOT NULL,
            product_id SMALLINT UNSIGNED NOT NULL,
            CONSTRAINT fk_category_id
            FOREIGN KEY (category_id) REFERENCES Category(id),
            CONSTRAINT fk_product_id
            FOREIGN KEY (product_id) REFERENCES Product(id),
            PRIMARY KEY (category_id, product_id))""")
        try:
            print("Creating table CPAssociation: ")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
        cursor.close()

    def insert_cpassociation_table(self, categories, barcodes):
        """Insert data into an already created

        category_product association table
        """
        cursor = self.db.cursor(dictionary=True, buffered=True)

        # Table composed of two columns
        add_product = ("""INSERT INTO CPAssociation
                       (category_id, product_id)
                       VALUES (%(category_id)s, %(product_id)s)
                       ON DUPLICATE KEY UPDATE category_id = category_id""")
        # Loop through principal category
        for category in api.category_list:
            # List of barcode for this principal category
            product_list = barcodes[category]
            # Find ids for each product as well as its subcategories
            for barcode in product_list:
                query = ("""SELECT id FROM Product
                         WHERE barcode = %s""")
                cursor.execute(query, (barcode,))
                product_id = [row['id'] for row in cursor][0]
                # List of categories related to this
                categories_list = categories[barcode]
                query = (
                    f"""SELECT id FROM Category
                        WHERE name IN
                        ({','.join('%s' for _ in categories_list)})
                        """)
                cursor.execute(query, tuple(categories_list))
                category_id_list = [row['id'] for row in cursor]
                # Creating one row
                for category_id in category_id_list:
                    data_product = dict(
                        zip(self.headers, [category_id, product_id]))
                    cursor.execute(add_product, data_product)

        self.db.commit()
        cursor.close()


class PSassociationBuilder:
    """This class manages the database

    with regard to the product-store association object
    """

    def __init__(self, db):
        """Initialise product_store table instances"""
        self.db = db
        self.headers = ["product_id", "store_id"]

    def create_psassociation_table(self):
        """Create the product_store association table"""
        cursor = self.db.cursor()
        table_description = (
            """CREATE TABLE PSAssociation (
            product_id SMALLINT UNSIGNED NOT NULL,
            store_id SMALLINT UNSIGNED NOT NULL,
            CONSTRAINT fk_food_id
            FOREIGN KEY (product_id) REFERENCES Product(id),
            CONSTRAINT fk_store_id
            FOREIGN KEY (store_id) REFERENCES Store(id),
            PRIMARY KEY (product_id, store_id))""")
        try:
            print("Creating table PSAssociation: ")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
        cursor.close()

    def insert_psassociation_table(self, stores, barcodes):
        """Insert data into an already created

        category_product association table
        """
        cursor = self.db.cursor(dictionary=True, buffered=True)
        add_product = ("""INSERT INTO PSAssociation
                       (product_id, store_id)
                       VALUES (%(product_id)s, %(store_id)s)
                       ON DUPLICATE KEY UPDATE product_id = product_id""")
        for category in api.category_list:
            product_list = barcodes[category]
            for barcode in product_list:
                query = ("""SELECT id FROM Product
                         WHERE barcode = %s""")
                cursor.execute(query, (barcode,))
                product_id = [row['id'] for row in cursor][0]
                # List of stores related to this product
                stores_list = stores[barcode]
                query = (
                    f"""SELECT id FROM Store
                        WHERE name IN
                        ({','.join('%s' for _ in stores_list)})
                        """)
                cursor.execute(query, tuple(stores_list))
                store_id_list = [row['id'] for row in cursor]
                for store_id in store_id_list:
                    data_product = dict(
                        zip(self.headers, [product_id, store_id]))
                    cursor.execute(add_product, data_product)

        self.db.commit()
        cursor.close()


def build():
    """Build the content of the data base"""
    pc = pcl.extract_data()
    product_rows = pc[0]
    categories = pc[1]
    stores = pc[2]
    barcodes = pc[3]
    ProductBuilder(db).create_product_table()
    ProductBuilder(db).insert_product_data(product_rows)
    ProductBuilder(db).create_favourite_table()
    CategoryBuilder(db).create_category_table()
    CategoryBuilder(db).insert_category_data(categories)
    StoreBuilder(db).create_store_table()
    StoreBuilder(db).insert_store_data(stores)
    CPassociationBuilder(db).create_cpassociation_table()
    CPassociationBuilder(db).insert_cpassociation_table(categories, barcodes)
    PSassociationBuilder(db).create_psassociation_table()
    PSassociationBuilder(db).insert_psassociation_table(stores, barcodes)


if __name__ == "__main__":
    build()
