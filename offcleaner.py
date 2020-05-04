# coding: utf-8
"""This module contains classes responsible for cleaning data
retrieved from Open Food Facts API"""
import offparser as pr


class ProductCleaner:

    attributes = ["product_name", ]

    def clean_data_from(self, parsed_data, category):
        """This function removes unecesseray data from what is downloaded for a given category"""

        # Parsed list of dictionaries with one product per dictionary for a
        # given category
        product_list = parsed_data[category]["products"]

        # Same structure as downloaded data (list of dictionaries) but with only needed attributes
        # product is a dictionary in the list
        clean_data = [{attribute: product.get(
            attribute) for attribute in ProductCleaner.attributes} for product in product_list]

        return clean_data

    def extract_attribute_list_per_category(
            self, parsed_data, category, attribute):
        """This function returns a list of values for a given atrribute for each product of a given category"""

        clean_data = self.clean_data_from(parsed_data, category)

        category_attribute_list = [
            product.get(attribute) for product in clean_data]
        return category_attribute_list

    def extract_attribute_list_per_product(
            self, parsed_data, category, wanted_product):
        """This function returns a list of attributes for a given product within a given category"""

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
                product.get(attribute) for attribute in ProductCleaner.attributes]

        return product_attribute_list


cleaner = ProductCleaner()
#unhealthy = cleaner.clean_data_from(pr.unhealthy_food_about,"Pizzas")
# print(unhealthy)

#extract_attribute_list_per_category = cleaner.extract_attribute_list_per_category(pr.unhealthy_food_about,"Pizzas","product_name")
# print(extract_attribute_list_per_category)

#extract_attribute_list_per_product = cleaner.extract_attribute_list_per_product(pr.unhealthy_food_about,"Pizzas",'Pizza 3 fromages' )
# print(extract_attribute_list_per_product)
