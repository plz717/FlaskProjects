import sqlite3
from flask import g
import logging


def init_db(app):
	with app.app_context(): # ???
		db = get_db()
		with open('data.sql', 'r') as f:
			db.cursor().executescript(f.read())
		db.commit()
		user_info = db.execute('select * from user_table').fetchall()
		logging.info("after initialized db, user_info:{}".format(user_info))


def get_db():
	db = sqlite3.connect('database')
	# command below will return the result as a namedtuple, 
	# so you can get result by its key or index
	db.row_factory = sqlite3.Row

	if not hasattr(g, 'db'):
		g.db = db  # ???
	return db


def close_db(e):
	if hasattr(g, 'db'):
		g.db.close()
		print("closed db.")

def init_db_for_app(app):
	app.teardown_appcontext(close_db)
	init_db(app)
