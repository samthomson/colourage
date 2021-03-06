import sqlite3



if __name__ == '__main__':

	#create/open db connection
	db = sqlite3.connect('database')

	cursor = db.cursor()
	"""
	cursor.execute('''
		CREATE TABLE files(id INTEGER, file TINYTEXT PRIMARY KEY,
	                   red UNSIGNED TINTYINT(1),
	                   green UNSIGNED TINTYINT(1),
	                   blue UNSIGNED TINTYINT(1))
	''')
	"""

	cursor.execute('''
		CREATE INDEX colour_index ON files (red, green, blue)
	''')


	db.commit()


	db.close()

