# coding: utf-8
"""This module contains needed cofiguration for getting data
from a given API"""


class ApiOff:

    #Endpoint and headers in line with Open Food Fcats guideline
    endpoint = "https://fr.openfoodfacts.org/cgi/search.pl?"
    response_header = {
        "User-Agent": "HealthyFoodSubstitute - MacOS Catalina - Version 10.15.4"}

    #list of chosen categories to be parsed from Open Food Facts Api
    category_list = [
        "Produits à tartiner salés",
        "Produits à tartiner sucrés",
        "Fromages",
        "Snacks salés",
        "Boissons à base de végétaux",
    ]

    attributes = ["product_name", "code", "stores", 'url', "categories_hierarchy"]

    @classmethod
    def healthy_choices_on(cls, wanted_category):
        """This classmethod contains criteria tags 
        to get healthy products for a given category, 
        from Open Food Facts Api"""
        healthy_choices = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": wanted_category,
            "tagtype_1": "nutrition_grades",
            "tag_contains_1": "contains",
            "tag_1": "A",
            "page_size": 1000,
            "json": "true"}
        return healthy_choices

    @classmethod
    def unhealthy_choices_on(cls, wanted_category):
        """This classmethod contains criteria tags 
        to get unhealthy products for a given category,
        from Open Food Facts Api"""
        unhealthy_choices = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": wanted_category,
            "tagtype_1": "nutrition_grades",
            "tag_contains_1": "contains",
            "tag_1": "E",
            "page_size": 1000,
            "json": "true"}
        return unhealthy_choices
