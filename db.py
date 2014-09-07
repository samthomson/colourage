import sqlite3



if __name__ == '__main__':


	#db = sqlite3.connect(':memory:')
	#create/open db connection
	db = sqlite3.connect('database')

	cursor = db.cursor()
	cursor.execute('''
		CREATE TABLE files(id INTEGER, file TINYTEXT PRIMARY KEY,
	                   red UNSIGNED TINTYINT(1),
	                   green UNSIGNED TINTYINT(1),
	                   blue UNSIGNED TINTYINT(1))
	''')
	db.commit()


	db.close()

