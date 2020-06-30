
"""Module to get data from open food facts Api"""

import requests

from .configuration import ApiOff as api


class ProductFetcher:
    """Class to retrieve data from an api"""

    @classmethod
    def get_data_about(cls, **kwargs):
        """Get data from a given endpoint"""
        response = requests.get(
            api.endpoint,
            headers=api.response_header,
            params=kwargs)
        if response.status_code != 200:
            raise Exception(
                f"Api connexion went wrong!-{response.status_code}")

        return response.json()['products']
