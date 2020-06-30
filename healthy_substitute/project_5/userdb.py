"""This module is responsible for connecting to the user database"""

import os

import mysql.connector

from mysql.connector import errorcode


config = {
    'user': os.environ.get('db_user'),
    'password': os.environ.get('db_pass'),
    'host': 'localhost',
    'database': 'offdb',
    'raise_on_warnings': True}


def connecting_to_database():
    """Establish connexion to user database"""
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        return cnx


db = connecting_to_database()
