"""Module to clean and extract retrieved data"""

from .offparser import ProductFetcher as pf

from .configuration import ApiOff as api


class ProductCleaner:
    """Class to get needed data from what is already parsed from an api"""

    @classmethod
    def clean_data(cls):
        """ Select data relative to valid predefined attribute values"""
        parsed_data = {category: [] for category in api.category_list}

        for category in parsed_data:
            page_number = 0
            # Loop through api until minimum number
            # of valid products per category is got
            while len(parsed_data.get(category)) < api.minimum_category_size:
                page_number += 1
                parsed_data.get(category).extend(pf.get_data_about(
                    **api.product_choices_on(category, page_number)))
                # Identify undesired imported products and remove them
                undesired_list = []
                for product in parsed_data.get(category):
                    if any(
                        (product.get(attr)is None or product.get(attr) == '')
                            for attr in api.attributes) or not(
                            product.get("code").isdigit()):
                        undesired_list.append(product)
                parsed_data[category] = [
                    product for product in parsed_data.get(
                        category) if product not in undesired_list]

        return parsed_data

    @classmethod
    def extract_data(cls):
        """Get attribute values for each product from parsed data"""
        parsed_data = cls.clean_data()
        product_rows = []
        categories = {}
        stores = {}
        barcodes = {}

        for category in parsed_data:
            product_barcode_list = []
            for product in parsed_data.get(category):
                product_barcode = product.get("code")
                # Define product attribute values list
                product_attribute_list = [product.get(
                    attribute) for attribute in api.product_characteristics]
                product_rows.append(product_attribute_list)
                # Define a (barcode, categories) dictionary structure
                product_subcategories = product.get("categories_hierarchy")
                product_categories = list(
                    set(product_subcategories + [category]))
                categories[product_barcode] = product_categories
                # Define a (barcode, stores) dictionary structure
                related_stores = product.get("stores").split(',')
                product_stores = [i for i in list(
                    set(related_stores)) if i and i != '']
                stores[product_barcode] = product_stores
                # Define a (category, barcodes) dictionary structure
                product_barcode = product.get("code")
                product_barcode_list.append(product_barcode)
            barcodes[category] = product_barcode_list

        return product_rows, categories, stores, barcodes
