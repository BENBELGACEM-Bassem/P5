# coding: utf-8
"""This module contains classes responsible for getting data
from an api"""
from configuration import ApiOff as api
import requests


class ProductFetcher:
    """This is a class for retrieving data from an api and making a local copy"""

    @classmethod
    def get_data_about(cls, **kwargs):
        response = requests.get(
            api.endpoint,
            headers=api.response_header,
            params=kwargs)
        if response.status_code !=200:
            raise ApiError (f"Something went wrong according to this code {response.status_code}")
        return response.json()

# Creating a dictionary containing parsed data for healthy products, for
# each category


HEALTHY_DATA = {category: ProductFetcher.get_data_about(
    **api.healthy_choices_on(category)) for category in api.category_list}

# Creating a dictionary containing parsed data for unhealthy products, for
# each category
UNHEALTHY_DATA = {category: ProductFetcher.get_data_about(
    **api.unhealthy_choices_on(category)) for category in api.category_list}
