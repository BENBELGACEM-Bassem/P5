"""Module to contain needed cofiguration for getting data"""


class ApiOff:
    """Class to encapsulate selected data about open food facts Api"""

    # Endpoint and headers in line with Open Food Fcats guideline
    endpoint = "https://fr.openfoodfacts.org/cgi/search.pl?"
    response_header = {
        "User-Agent": "HealthySubstitute - MacOS Catalina - Version 10.15.4"}

    # list of chosen categories to be parsed from Open Food Facts Api
    category_list = [
        "Produits à tartiner salés",
        "Produits à tartiner sucrés",
        "Fromages",
        "Snacks salés",
        "Boissons à base de végétaux"
    ]

    attributes = ["product_name", "nutrition_grades",
                  'url', "stores", "code", "categories_hierarchy"]
    product_characteristics = [
        "code", "product_name", "nutrition_grades", "url"]

    minimum_category_size = 1000

    @classmethod
    def product_choices_on(cls, wanted_category, page_number):
        """Contain criteria to get healthy products for a given category"""
        product_choices = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": wanted_category,
            "page_size": 1000,
            "page": page_number,
            "json": "true"}
        return product_choices
