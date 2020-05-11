# coding: utf-8
"""This module contains classes responsible for cleaning data
retrieved from Open Food Facts API"""
import offparser as pr


class ProductCleaner:

    """This is a class for getting needed data from what is already parsed from an api"""

    def clean_data_from(self, parsed_data, category):
        """This function removes unecesseray data from what is downloaded for a given category"""

        # List of products definition for a given category
        # Each product is represented by a dictionary structure inside this list
        product_list = parsed_data[category]["products"]

        # Only needed attributes are kept for each product 
        clean_data = [{attribute: product.get(
            attribute) for attribute in pr.api.attributes} for product in product_list]

        return clean_data

    def extract_attribute_list_per_category(
            self, parsed_data, category, attribute):
        """for a given atrribute, for a given category, this function returns the list of this attribute values """

        clean_data = self.clean_data_from(parsed_data, category)

        category_attribute_list = [
            product.get(attribute) for product in clean_data]
        return category_attribute_list

    def extract_attribute_list_per_product(
            self, parsed_data, category, wanted_product):
        """For a given product,within a given category, this function returns a list of attribute value """

        clean_data = self.clean_data_from(parsed_data, category)

        # Getting the dictionary with the same product name as the one we are
        # looking for
        products = [
            product for product in clean_data if product["product_name"] == wanted_product]

        # Getting all attributes for the wanted product in case it exists
        # within the given category
        if products:

            product = products[0]

            product_attribute_list = [
                product.get(attribute) for attribute in pr.api.attributes]

        return product_attribute_list


cleaner = ProductCleaner()
healthy = cleaner.clean_data_from(pr.healthy_food_about,"Fromages")
print(len(healthy))

# extract_attribute_list_per_category = cleaner.extract_attribute_list_per_category(pr.healthy_food_about,"Fromages","product_name")
# print(extract_attribute_list_per_category)

# extract_attribute_list_per_product = cleaner.extract_attribute_list_per_product(pr.unhealthy_food_about,"Fromages",'Kiri' )
# print(extract_attribute_list_per_product)
