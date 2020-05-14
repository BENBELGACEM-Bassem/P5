# coding: utf-8
"""This module is responsible for managing a provided database
by creating tables, inserting and querying data from it """

from dbidentifier import config
import mysql.connector
from mysql.connector import errorcode

class DbPlanner:

	def __init__(self, **tables):
		for table_title, table_description in tables.items():
			setattr(self, table_title, table_description)

	@classmethod
	def connecting_to_data_base(cls):
		try:
		  cnx = mysql.connector.connect(**config)
		except mysql.connector.Error as err:
		  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		    print("Something is wrong with your user name or password")
		  elif err.errno == errorcode.ER_BAD_DB_ERROR:
		    print("Database does not exist")
		  else:
		    print(err)

	def creating_tables(self):
		cls.connecting_to_data_base()
		cursor = cnx.cursor()
		for self.table_title, self.table_description in self.tables.items():
		    try:
		        print(f"Creating table {self.table_title}: ", end='')
		        cursor.execute(self.table_description)
		    except mysql.connector.Error as err:
		        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
		            print("already exists.")
		        else:
		            print(err.msg)
		    else:
		        print("OK")

		cursor.close()

	def insertng_data(self):











	def main():
		pass
		# tables = 
		#cnx.close()

if __name__ == '__main__':
	main()

