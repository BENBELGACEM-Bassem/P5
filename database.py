# coding: utf-8
"""This module is responsible for connecting to the user database"""

from dbidentifier import config
import mysql.connector
from mysql.connector import errorcode

def connecting_to_database():
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