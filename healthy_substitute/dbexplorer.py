"""This module is responsible for

defining tools to explore the data base
"""

from models import(Product, Category)


class UseCase:
    """This class encapsulates needed tools to implement

    an explorator data base use case
    """

    @classmethod
    def display_categories(cls):
        """Display each category name and id"""
        principal_category_list = Category.objects.get_principal_categories()
        category_id_list = [
            category.id for category in principal_category_list]
        categories_string = ""
        for category in principal_category_list:
            categories_string += str(category) + '\n'
        return categories_string, category_id_list

    @classmethod
    def display_products(cls, category_id):
        """Display product attributes"""
        display_list = Product.objects.get_products_for_category(category_id)
        products_string = ""
        barcode_list = []
        for product in display_list:
            products_string += repr(product) + '\n'
            barcode_list.append(product.barcode)
        return products_string, barcode_list

    @classmethod
    def find_substitute(cls, barcode_to_substitute):
        """Get a substitute product"""
        substitute_product = Product.objects.get_substitute(
            barcode_to_substitute)
        product = substitute_product[0]
        store = substitute_product[1]
        substitute_string = str((str(product), str(store))) + '\n'
        return substitute_string, substitute_product

    @classmethod
    def save(cls, *args):
        """Save a favourite product"""
        return Product.objects.save(args[0], args[1])

    @classmethod
    def display_favourite_table(cls):
        """Display favourite products saved"""
        table_content = Product.objects.get_favourite_table()
        if isinstance(table_content, str):
            return table_content
        else:
            table_of_string = ""
            for (product, store) in table_content:
                table_of_string += str((str(product), str(store))) + '\n'
            return table_of_string