
from flask import request, Blueprint, render_template, redirect, url_for, flash
import logging
from .db import get_db


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods = ('GET', 'POST'))
def register():
	if request.method == 'POST':
		logging.info("post method in register!")
		username = request.form['username']
		password = request.form['password']

		if username is None:
			error = 'username is required!'
		elif password is None:
			error = 'password is required!'
		elif get_db().execute('select * from user_table where username = (?)', (username, )).fetchone() is not None:
			error = "{} has registered already!".format(username)
		else:
			error = None

		if error is None:
			# insert user data in database
			db = get_db()
			db.execute('insert into user_table values (?, ?)', (username, password))
			db.commit()
			return render_template('auth/login.html')

	logging.info('you are using get method!')
	return render_template('auth/register.html')


@auth_bp.route('/auth/login', methods = ('GET', 'POST'))
def login():
	if request.method == 'POST':
		# if user input nothing, 
		# then username and password will be both '' rather than None!
		username = request.form['username']
		password = request.form['password']
		print("username:{}, password:{}".format(username, password))
		assert username is not None
		db = get_db()
		result = db.execute('select * from user_table where username = (?)', (username, )).fetchone()
		print('result:', result)

		error = None
		if result is None:
			error = 'incorrect username!'
		elif result['password'] != password: 
			error = 'incorrect password!'

		if error is None:
			return redirect(url_for('index'))

		flash(error)

	return render_template('auth/login.html')



