"""This module is responsible for managing a provided database by creating

tables, inserting and querying data from its
"""

import mysql.connector

from mysql.connector import errorcode

import models

import offcleaner as cl

from offcleaner import ProductCleaner as pc


class ProductRepository:
    """This class manages the database with regard to the product object"""

    def __init__(self, db):
        """Initialise product table instance"""
        self.db = db
        self.headers = ["id", "barcode", "name", "nutrition_grade", "url"]

    def create_product_table(self):
        """Create the product table"""
        cursor = self.db.cursor()
        table_description = (
            "CREATE TABLE Product ("
            "id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,"
            "barcode BIGINT NOT NULL UNIQUE,"
            "name VARCHAR(255),"
            "nutrition_grade CHAR(1) NOT NULL,"
            "url TEXT NOT NULL,"
            "PRIMARY KEY (id))")
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

    def insert_product_data(self):
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
        for parsed_data in (
                cl.pr.HEALTHY_DATA,
                cl.pr.UNHEALTHY_DATA):
            for category in cl.pr.api.category_list:
                for barcode in (
                    pc.extract_attribute_values_per_category(
                        parsed_data, category, "code")):
                    product_row = pc.extract_attribute_list_per_product(
                        parsed_data, category, barcode,
                        "code", "product_name", "nutrition_grades", 'url')
                    data_product = dict(
                        zip(self.headers, [None, *product_row]))
                    cursor.execute(add_product, data_product)
        self.db.commit()
        cursor.close()

    def get_products_for_category(self, category_id):
        """Get a list of unhealthy product candidates

        for a given Category instance
        """
        cursor = self.db.cursor(dictionary=True, buffered=True)
        # Get random barcode from unhealthy product list for the given
        # category_name
        query = """SELECT p.barcode, p.name, p.nutrition_grade, p.url
        FROM Product AS p
        JOIN CPAssociation AS cp
        ON p.id = cp.product_id
        JOIN Category AS c
        ON cp.category_id = c.id
        WHERE p.nutrition_grade = 'e'
        AND c.id = %(id)s
        ORDER BY RAND()
        LIMIT 10"""
        cursor.execute(query, {'id': category_id})
        displayed_products = [
            models.Product(
                row['barcode'],
                row['name'],
                row['nutrition_grade'],
                row['url']) for row in cursor]
        cursor.close()
        # list of Product instances
        return displayed_products

    def get_substitute(self, barcode_to_substitute):
        """Get a product substitute for a given product"""
        cursor = self.db.cursor(dictionary=True, buffered=True)
        # Getting subcategories id for the barcode to be substituted
        query0 = ("""SELECT c.id AS subcategory_id
                  FROM Product AS p
                  JOIN CPAssociation AS cp
                  ON p.id = cp.product_id
                  JOIN Category AS c
                  ON cp.category_id = c.id
                  WHERE p.barcode = %(barcode)s""")
        cursor.execute(query0, {'barcode': barcode_to_substitute})
        list1 = [row['subcategory_id'] for row in cursor]
        # Getting the substitute product id (intermediate step)
        query1 = f""" SELECT id, MAX(subcategories_number)
                 FROM(
                     SELECT p.id, COUNT(*) AS subcategories_number
                     FROM Product AS p
                     JOIN CPAssociation AS cp
                     ON p.id = cp.product_id
                     JOIN Category AS c
                     ON cp.category_id = c.id
                     WHERE c.id IN ({','.join('%s' for _ in list1)})
                     AND p.nutrition_grade = 'a'
                     GROUP BY p.id ) AS Intermediate
                     GROUP BY id"""
        cursor.execute(query1, tuple(list1))
        substitute_id = [row['id'] for row in cursor][0]
        # Getting the substitute product
        query2 = """SELECT p.barcode, p.name, p.nutrition_grade, p.url, s.name AS store
        FROM Product AS p
        JOIN PSAssociation AS ps
        ON p.id = ps.product_id
        JOIN store AS s
        ON ps.store_id = s.id
        WHERE p.id = %(id)s"""
        cursor.execute(query2, {'id': substitute_id})
        substitute_product = [
            (models.Product(
                row['barcode'],
                row['name'],
                row['nutrition_grade'],
                row['url']),
                models.Store(
                row['store'])) for row in cursor][0]
        cursor.close()
        # (product, store) instance tuple
        return substitute_product

    def create_favourite_table(self):
        """Create the favourite product table"""
        cursor = self.db.cursor()
        table_description = (
            "CREATE TABLE Favourite_product ("
            "barcode BIGINT,"
            "name VARCHAR(255),"
            "nutrition_grade CHAR(1) NOT NULL,"
            "url TEXT NOT NULL,"
            "store VARCHAR(255) NOT NULL,"
            "PRIMARY KEY (barcode))")
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

    def save(self, product, shop):
        """Save user favourite products"""
        cursor = self.db.cursor()
        substitute_product = {
            'barcode': product.barcode,
            'name': product.name,
            'nutrition_grade': product.nutrition_grade,
            'url': product.url,
            'store': shop.name}
        add_product = (
            """INSERT INTO Favourite_product
            (barcode, name, nutrition_grade, url, store)
            VALUES (
            %(barcode)s,
            %(name)s,
            %(nutrition_grade)s,
            %(url)s,
            %(store)s)"
            ON DUPLICATE KEY UPDATE barcode = barcode""")
        cursor.execute(add_product, substitute_product)
        self.db.commit()
        cursor.close()

    def get_favourite_table(self):
        """Get user favourite table"""
        cursor = self.db.cursor(dictionary=True, buffered=True)
        query = "SELECT * FROM Favourite_product"
        cursor.execute(query)
        if not cursor.rowcount:
            table_content = "Table of favourites is empty!"
        else:
            table_content = [
                (models.Product(
                    row['barcode'],
                    row['name'],
                    row['nutrition_grade'],
                    row['url']),
                    models.Store(
                    row['store'])) for row in cursor]
        cursor.close()
        # (product, store) instance couple list
        return table_content

    def get_favourite_product(self, barcode):
        """Get user favourite products"""
        cursor = self.db.cursor()
        query = """SELECT fp.barcode, fp.name,
                fp.nutrition_grade, fp.url, fp.store
        FROM Favourite_product AS fp
        WHERE barcode = %s"""
        cursor.execute(query, (barcode,))
        favourite_product = [
            (models.Product(
                row['barcode'],
                row['name'],
                row['nutrition_grade'],
                row['url']),
                models.Store(
                row['store']))
            for row in cursor][0]
        cursor.close()
        # (product, store) instance couple list
        return favourite_product


class CategoryRepository:
    """This class manages the database with regard to the category object"""

    def __init__(self, db):
        """Initialise category table instances"""
        self.db = db
        self.headers = ["id", "name"]

    def create_category_table(self):
        """Create the category table"""
        cursor = self.db.cursor()
        table_description = (
            "CREATE TABLE Category ("
            "id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,"
            "name VARCHAR(255) NOT NULL UNIQUE,"
            "PRIMARY KEY (id))")
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

    def insert_category_data(self):
        """Insert category data into an already created category table"""
        cursor = self.db.cursor()
        add_product = ("INSERT INTO Category"
                       "(id, name)"
                       "VALUES (%(id)s, %(name)s)"
                       "ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id)")
        complete_category_list = pc.all_categories_involved(
            cl.pr.HEALTHY_DATA, cl.pr.UNHEALTHY_DATA)
        for category in complete_category_list:
            category_row = [None, category]
            data_category = dict(zip(self.headers, category_row))
            cursor.execute(add_product, data_category)
        self.db.commit()
        cursor.close()

    def get_principal_categories(
            self, predefined_list=cl.pr.api.category_list):
        """Display principal categories"""
        cursor = self.db.cursor(dictionary=True, buffered=True)
        query = f"""SELECT * FROM Category AS c
                WHERE c.name IN ({','.join('%s' for _ in predefined_list)})"""
        cursor.execute(query, tuple(predefined_list))
        principal_category_list = [
            models.Category(row['id'], row['name']) for row in cursor]
        cursor.close()
        # Category instance list
        return principal_category_list


class StoreRepository:
    """Manage the database with regard to the store object"""

    def __init__(self, db):
        """Initialise store table instances"""
        self.db = db
        self.headers = ["id", "name"]

    def create_store_table(self):
        """Create the store table"""
        cursor = self.db.cursor()
        table_description = (
            "CREATE TABLE Store ("
            "id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,"
            "name VARCHAR(255) NOT NULL UNIQUE,"
            "PRIMARY KEY (id))")
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

    def insert_store_data(self):
        """Insert store data into an already created table"""
        cursor = self.db.cursor()
        add_product = ("INSERT INTO Store"
                       "(id, name)"
                       "VALUES (%(id)s, %(name)s)"
                       "ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id)")
        for store in pc.all_stores_involved(
                cl.pr.HEALTHY_DATA, cl.pr.UNHEALTHY_DATA):
            data_product = dict(
                zip(self.headers, [None, store]))
            cursor.execute(add_product, data_product)
        self.db.commit()
        cursor.close()


class CPAssociationRepository:
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

    def insert_cpassociation_table(self):
        """Insert data into an already created

        category_product association table
        """
        cursor = self.db.cursor(dictionary=True, buffered=True)
        add_product = ("INSERT INTO CPAssociation "
                       "(category_id, product_id) "
                       "VALUES (%(category_id)s, %(product_id)s)")
        for parsed_data in (
                cl.pr.HEALTHY_DATA,
                cl.pr.UNHEALTHY_DATA):
            for category in cl.pr.api.category_list:
                query = ("SELECT id FROM Category "
                         "WHERE name = %s")
                cursor.execute(query, (category,))
                # List composed of one element: the principal category id
                principal_category_id = [row['id'] for row in cursor]
                # List of barcode for this principal category
                product_list = pc.extract_attribute_values_per_category(
                    parsed_data, category, "code")

                for barcode in product_list:

                    query = ("SELECT id FROM Product "
                             "WHERE barcode = %s")
                    cursor.execute(query, (barcode,))
                    product_id = [row['id'] for row in cursor][0]

                    subcategories_list = sum(
                        pc.extract_attribute_list_per_product
                        (parsed_data, category, barcode,
                         "categories_hierarchy"), [])
                    query = (
                        f"""SELECT id FROM Category"
                            WHERE name IN
                            ({','.join('%s' for _ in subcategories_list)})
                            """)
                    cursor.execute(query, tuple(subcategories_list))
                    subcategories_id_list = [row['id'] for row in cursor]
                    # All categories id related to this product
                    category_id_list = list(
                        set(subcategories_id_list + principal_category_id))
                    # Creating the row
                    for category_id in category_id_list:
                        data_product = dict(
                            zip(self.headers, [category_id, product_id]))
                        cursor.execute(add_product, data_product)

        self.db.commit()
        cursor.close()


class PSAssociationRepository:
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
            store_id SMALLINT UNSIGNED NOT NULL,"
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

    def insert_psassociation_table(self):
        """Insert data into an already created

        category_product association table
        """
        cursor = self.db.cursor(dictionary=True, buffered=True)
        add_product = ("INSERT INTO PSAssociation"
                       "(product_id, store_id)"
                       "VALUES (%(product_id)s, %(store_id)s)")
        for parsed_data in (
                cl.pr.HEALTHY_DATA,
                cl.pr.UNHEALTHY_DATA):

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
