# coding: utf-8
"""This module contains classes responsible for getting data
from an api"""
from configuration import ApiOff as api
import requests


class ProductFetcher:
	"""This is a class for creating object to retrieve data from an api""" 
	def get_data_about(self, **kwargs):
		response = requests.get(
            api.endpoint,
            headers=api.response_header,
            params=kwargs)
		return response.json()

	def __repr__(self):
		return " this is an object to parse Api"


fetcher = ProductFetcher()
#Creating a dictionary containing parsed data for healthy products, for each category 
healthy_food_about = {category: fetcher.get_data_about(
    **api.healthy_choices_on(category)) for category in api.category_list}
#Creating a dictionary containing parsed data for unhealthy products, for each category 
unhealthy_food_about = {category: fetcher.get_data_about(
    **api.unhealthy_choices_on(category)) for category in api.category_list}


liste = (healthy_food_about)["Pizzas"]["products"][0]
print(liste.keys())
# print((healthy_data_downloaded_about)["pizza"]["products"][1])
