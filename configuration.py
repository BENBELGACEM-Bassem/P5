# coding: utf-8
"""This module contains needed cofiguration for getting data
from a given API"""


class ApiOff:

    endpoint = "https://fr.openfoodfacts.org/cgi/search.pl?"
    response_header = {
        "User-Agent": "HealthyFoodSubstitute - MacOS Catalina - Version 10.15.4"}
    category_list = [
        "Produits à tartiner sucrés",
        "Matières grasses à tartiner",
        "Céréales pour petit-déjeuner",
        "Huiles",
        "Fromages",
        "Snacks salés",
        "Snacks sucrés",
        "Pizzas",
        "Desserts",
        "Boissons à base de végétaux",
    ]

    @classmethod
    def healthy_choices_on(cls, wanted_category):
        healthy_choices = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": wanted_category,
            "tagtype_1": "nutrition_grades",
            "tag_contains_1": "contains",
            "tag_1": "A",
            "json": "true"}
        return healthy_choices

    @classmethod
    def unhealthy_choices_on(cls, wanted_category):
        unhealthy_choices = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": wanted_category,
            "tagtype_1": "nutrition_grades",
            "tag_contains_1": "contains",
            "tag_1": "E",
            "json": "true"}
        return unhealthy_choices
