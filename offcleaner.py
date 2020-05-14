# coding: utf-8
"""This module contains classes responsible for cleaning data
retrieved from Open Food Facts API"""
import offparser as pr


class ProductCleaner:

    """This is a class for getting needed data from what is already parsed from an api"""

    def filtered_data_from(self, parsed_data, category):
        """This function removes unecesseray data from what is downloaded for a given category"""

        # List of products definition for a given category
        # Each product is represented by a dictionary structure inside this
        # list
        product_list = parsed_data[category]["products"]

        # Only needed attributes are kept for each product
        filtered_data = [{attribute: product.get(
            attribute) for attribute in pr.api.attributes} for product in product_list]

        return filtered_data

    def extract_attribute_values_per_category(
            self, parsed_data, category, attribute):
        """for a given atrribute, for a given category, this function returns
        that attribute value for each product of that category   """

        filtered_data = self.filtered_data_from(parsed_data, category)

        category_attribute_values = {product.get("code"): product.get(
            attribute) for product in filtered_data}

        return category_attribute_values

    def extract_attribute_list_per_product(
            self, parsed_data, category, barecode):
        """For a given product,within a given category, this function returns
        a list of that product attribute values """

        filtered_data = self.filtered_data_from(parsed_data, category)

        # Getting the dictionary with the same product as the one we are
        # looking for
        products = [
            product for product in filtered_data if product.get("code") == barecode]

        # Getting all attributes for the wanted product in case it exists
        # within the given category
        if products:

            product = products[0]

            product_attribute_list = [
                product.get(attribute) for attribute in pr.api.attributes]

            return product_attribute_list

        return " This product is unknown"

    def get_sub_categories(self, parsed_data, category):
        """For a given category, this function returns sub categories related list
         for each product of that category without duplication """

        # Getting the list of sub categories
        category_attribute_values = self.extract_attribute_values_per_category(
            parsed_data, category, "categories_hierarchy")

        # Flattening the result nested list and removing duplicates
        sub_categorie_list = list(set(
            [item for attribute in category_attribute_values.values() for item in attribute]))

        return sub_categorie_list

    def get_stores(self, parsed_data, category):
        """For a given category, this function returns stores related list
         for each product of that category without duplication """

        # Getting the list of stores
        category_attribute_values = self.extract_attribute_values_per_category(
            parsed_data, category, "stores")

        # Flattening the result nested list and removing duplicates
        stores_list = list(set(category_attribute_values.values()))

        return stores_list


cleaner = ProductCleaner()



# testing

# healthy = cleaner.filtered_data_from(pr.healthy_food_about, "Fromages")
# print(len(healthy))


# extract_attribute_list_per_category = cleaner.extract_attribute_list_per_category(pr.healthy_food_about,"Fromages","product_name")
# print(extract_attribute_list_per_category)

# extract_attribute_list_per_product = cleaner.extract_attribute_list_per_product(pr.unhealthy_food_about,"Fromages",'Kiri' )
# print(extract_attribute_list_per_product)

# hierarchy = cleaner.get_sub_categories(pr.healthy_food_about, "Snacks salés")
# hierarchy = cleaner.get_stores(pr.healthy_food_about, "Fromages")
# hierarchy = cleaner.extract_attribute_values_per_category(pr.healthy_food_about,"Snacks salés","categories_hierarchy")
# print(hierarchy)
