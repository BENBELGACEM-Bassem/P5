"""Module to clean retrieved data"""

import offparser as pr


class ProductCleaner:
    """Class to get needed data from what is already parsed from an api"""

    @classmethod
    def filtered_data_from(cls, parsed_data, category):
        """Remove unecesseray data from downloaded data for a given category"""
        # List of products definition for a given category
        # Each product is represented by a dictionary structure
        products = parsed_data.get(category).get("products")

        # Only needed attributes are kept for each product
        filtered_data = [{attr: product.get(
            attr) for attr in pr.api.attributes} for product in products]

        return filtered_data

    @classmethod
    def extract_attribute_values_per_category(
            cls, parsed_data, category, attribute):
        """For a given atrribute, for a given category, this function returns

        that attribute value for each product of that category
        """
        filtered_data = cls.filtered_data_from(parsed_data, category)
        # Checking that the attribute is known
        if attribute in pr.api.attributes:
            category_attribute_values = [product.get(
                attribute) for product in filtered_data if product.get("code")]
            return category_attribute_values
        return "This attribute is unknown"

    @classmethod
    def extract_attribute_list_per_product(
            cls, parsed_data, category, barcode, *attribute_list):
        """For a given product,within a given category, this function returns

        a list of that product attribute values
        """
        filtered_data = cls.filtered_data_from(parsed_data, category)

        # Finding our product using the given barcode
        products = [
            prod for prod in filtered_data if prod.get("code") == barcode]

        # Getting attributes values within a list
        if products and all(
                attr in pr.api.attributes for attr in attribute_list):
            product = products[0]
            product_attribute_list = [
                product.get(attribute) for attribute in attribute_list]
            return product_attribute_list

        # Handling error in case of an unknown product or attributes
        elif products and not (
                all(attr in pr.api.attributes for attr in attribute_list)):
            return "All attributes are not known"
        elif not products and all(
                attr in pr.api.attributes for attr in attribute_list):
            return "This product is unknown"
        return " Product and attributes are unknown"

    @classmethod
    def all_categories_involved(cls, *args):
        """Get the complete list of categories involved"""
        subcategories = []
        for parsed_data in args:
            for category in pr.api.category_list:
                # Flatten the subcategories list
                nested_list = cls.extract_attribute_values_per_category(
                    parsed_data, category, "categories_hierarchy")
                flatten_list = sum(nested_list, [])
                # Joining sub categories from each principal category
                subcategories.extend(flatten_list)
        # Adding principal categories to the list
        complete_category_list = list(
            set((pr.api.category_list + subcategories)))

        return complete_category_list

    @classmethod
    def all_stores_involved(cls, *args):
        """Get the complete list of categories involved"""
        complete_store_list = []
        for parsed_data in args:
            for category in pr.api.category_list:
                for barcode in list(
                        set(
                            cls.extract_attribute_values_per_category(
                                parsed_data, category, "code"))):
                    # Get list of attributes values per product, then use split
                    # to get a list of individual store name
                    related_stores = cls.extract_attribute_list_per_product(
                        parsed_data, category, barcode, "stores")

                    if related_stores[0] and (related_stores[0] != ''):

                        complete_store_list.extend(
                            related_stores[0].split(','))
        # Final step of removing possible empty string
        complete_store_list = [i for i in list(
            set(complete_store_list)) if i != '']

        return complete_store_list

    @classmethod
    def all_stores_involved_per_product(cls, parsed_data, category, barcode):
        """Get the complete list of categories involved per product"""
        complete_store_list = []
        related_stores = cls.extract_attribute_list_per_product(
            parsed_data, category, barcode, "stores")

        if related_stores[0] and related_stores[0] != '':
            complete_store_list.extend(related_stores[0].split(','))

        complete_store_list = [i for i in list(
            set(complete_store_list)) if i != '']

        return complete_store_list