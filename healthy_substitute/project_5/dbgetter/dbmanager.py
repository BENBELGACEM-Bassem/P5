"""This module is responsible for managing a provided database by creating

tables, inserting and querying data from its
"""

from . import models


class ProductRepository:
    """This class manages the database with regard to the product object"""

    def __init__(self, db):
        """Initialise product table instance"""
        self.db = db
        self.headers = ["id", "barcode", "name", "nutrition_grade", "url"]

    def get_products_for_category(self, category_id):
        """Get a list of product candidates

        for a given Category instance
        """
        cursor = self.db.cursor(dictionary=True, buffered=True)
        # Get random barcode from product list for the given
        # category_name
        query = """SELECT p.barcode, p.name, p.nutrition_grade, p.url
        FROM Product AS p
        JOIN CPAssociation AS cp
        ON p.id = cp.product_id
        JOIN Category AS c
        ON cp.category_id = c.id
        WHERE c.id = %(id)s
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
        # Getting subcategories_id and grade for the barcode to be substituted
        query0 = ("""SELECT p.nutrition_grade, c.id AS subcategory_id
                  FROM Product AS p
                  JOIN CPAssociation AS cp
                  ON p.id = cp.product_id
                  JOIN Category AS c
                  ON cp.category_id = c.id
                  WHERE p.barcode = %(barcode)s""")
        cursor.execute(query0, {'barcode': barcode_to_substitute})
        query0_response = [
            (row['subcategory_id'],
             row['nutrition_grade']) for row in cursor]
        subcategories = [i[0] for i in query0_response]
        grade_to_substitute = query0_response[0][1]
        # Getting a list of substitute product candidates (intermediate step)
        # sharing subcategories with the product to substitute
        query1 = f"""SELECT p.id, p.nutrition_grade, COUNT(*) AS subcategories_number
            FROM Product AS p
            JOIN CPAssociation AS cp ON p.id = cp.product_id
            JOIN Category AS c ON cp.category_id = c.id
            WHERE c.id IN ({','.join('%s' for _ in subcategories)})
            GROUP BY p.id
            ORDER BY subcategories_number DESC"""
        cursor.execute(query1, tuple(subcategories))
        query1_response = [(
            row['id'], row['nutrition_grade'], row['subcategories_number']
        ) for row in cursor]
        # Find, in the candidates list, a healthier product(lower grade)
        # sharing a maximum number of subcategories
        for i in query1_response:
            if i[1] < grade_to_substitute:
                # Getting all the substitute product attributes
                substitute_id = i[0]
                query2 = """SELECT p.id, p.barcode, p.name, p.nutrition_grade, p.url,
                GROUP_CONCAT(store.name)
                FROM Product AS p
                JOIN PSAssociation AS ps
                ON p.id = ps.product_id
                JOIN store
                ON ps.store_id = store.id
                WHERE p.id = %(id)s
                GROUP BY p.id"""
                cursor.execute(query2, {'id': substitute_id})
                substitute_product = [
                    (models.Product(
                        row['barcode'],
                        row['name'],
                        row['nutrition_grade'],
                        row['url'],
                        row['id']),
                        models.Store(
                        row['GROUP_CONCAT(store.name)'])) for row in cursor][0]
                break
            else:
                substitute_product = (
                    "Sorry! There is no healthier product to propose")
        cursor.close()
        # (product, store) tuple of two instances or a string message
        return substitute_product

    def save(self, product):
        """Save user favourite products"""
        cursor = self.db.cursor(dictionary=True, buffered=True)

        add_to_favourite = (
            """INSERT INTO Favourite_product (id) VALUES (%s)
            ON DUPLICATE KEY UPDATE id = id""")
        cursor.execute(add_to_favourite, (product.id,))

        self.db.commit()
        cursor.close()

    def get_favourite_list(self):
        """Get user favourite table"""
        cursor = self.db.cursor(dictionary=True, buffered=True)
        query = """SELECT p.id, p.barcode, p.name, p.nutrition_grade, p.url,
                GROUP_CONCAT(store.name)
                FROM Product AS p
                JOIN PSAssociation AS ps
                ON p.id = ps.product_id
                JOIN store
                ON ps.store_id = store.id
                JOIN Favourite_product AS fp
                ON p.id = fp.id
                GROUP BY p.id"""
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
                    row['GROUP_CONCAT(store.name)'])) for row in cursor]
        cursor.close()
        # (product, store) list of tuple instances
        return table_content


class CategoryRepository:
    """This class manages the database with regard to the category object"""

    def __init__(self, db):
        """Initialise category table instances"""
        self.db = db
        self.headers = ["id", "name"]
        self.principal_categories = [
            "Produits à tartiner salés",
            "Produits à tartiner sucrés",
            "Fromages",
            "Snacks salés",
            "Boissons à base de végétaux"]

    def get_principal_categories(self):
        """Display principal categories"""
        cursor = self.db.cursor(dictionary=True, buffered=True)
        query = f"""SELECT * FROM Category AS c
                WHERE c.name IN
                ({','.join('%s' for _ in self.principal_categories)})"""
        cursor.execute(query, tuple(self.principal_categories))
        principal_category_instance_list = [
            models.Category(row['id'], row['name']) for row in cursor]
        cursor.close()
        # Category instance list
        return principal_category_instance_list


class StoreRepository:
    """Manage the database with regard to the store object"""

    def __init__(self, db):
        """Initialise store table instances"""
        self.db = db
        self.headers = ["id", "name"]
