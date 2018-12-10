#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Cette application met en place un serveur web permettant d'insérer X enregistrements
    dans une table d'une base de données SQL via l'URL suivante
    http://adress/mysql/<nombre_enregristrements>

    Par exemple :
    * http://adress/mysql/1
    * http://adress/mysql/42
    * http://adress/mysql/999
"""

from bottle import Bottle, response, hook, static_file
import os, sys, socket, json, datetime

rootPath = os.path.dirname(os.path.abspath(__file__))
app = Bottle()

@app.route('/mysql/<insertNumber>', ['GET'])
def sqlQuery(insertNumber):
	""" Exécute la requête <query> reçue en paramètre """
	import pymysql.cursors
	result = {}
	connection = pymysql.connect(host=os.environ['MYSQL_HOST'],
                    user=os.environ['MYSQL_USER'],
                    password=os.environ['MYSQL_USER_PASSWORD'],
                    db=os.environ['MYSQL_DB_NAME'],
                    cursorclass=pymysql.cursors.DictCursor)

	
	print(insertNumber + ' insertions MySQL à réaliser')
	try:
		with connection.cursor() as cursor:
			# Create a new record
			cursor.execute("CREATE TABLE IF NOT EXISTS `test` (`login` varchar(20), `password` varchar(100)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;")
			for x in range(int(insertNumber)):
				cursor.execute("INSERT INTO test VALUES ('John', 'DOE')")
		connection.commit() 

		with connection.cursor() as cursor:
			# Read a single record
			cursor.execute("SELECT * FROM test")
			result = cursor.fetchall()
			print(result)
	except Exception as e:
		print(e)
	finally:
		connection.close()
		return json.dumps(result)


if __name__ == '__main__':
	print("Bottle server start")

	app.run(
		host="0.0.0.0",
		port=80,
		reloader=False,
		debug=False
	)