"""This module is responsible for identifying user data bas

and providing needed parameters to connect to Mysql server
"""

import os

config = {
    'user': os.environ.get('db_user'),
    'password': os.environ.get('db_pass'),
    'host': 'localhost',
    'database': 'offdb',
    'raise_on_warnings': True}
