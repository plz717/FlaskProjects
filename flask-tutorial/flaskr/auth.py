# coding=utf-8

import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
import logging

logging.basicConfig(level = logging.DEBUG)

logging.debug("in auth.py, __name__:{}".format(__name__)) # flaskr.auth
bp = Blueprint('auth', __name__, url_prefix = '/auth')

@bp.route('/register', methods = ('GET', 'POST'))
def register():
	logging.debug("in register fun, request.method:{}".format(request.method))
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None

		if not username:
			error = 'username is required'
		# use elif instead of if!!! or the error will be override!
		elif not password:
			error = 'password is required'
		elif db.execute('select id from user where username = ?', (username, )).fetchone() is not None:
			error = 'user {} is already registered.'.format(username)

		print("in register fun, error:", error)
		if error is None:
			db.execute('insert into user (username, password) values (?, ?)', (username, generate_password_hash(password)))
			db.commit()
			# 重定向到登录页面
			return redirect(url_for('auth.login'))

		flash(error)

	# 当用户第一次访问'auth/register'时，会返回一个注册表单
	return render_template('auth/register.html')


@bp.route('/login', methods = ('GET', 'POST'))
def login():
	logging.debug("in login fun, request.method:{}".format(request.method))
	if request.method == 'POST':
		logging.debug("in login fun, request.form['username']:{}".format(request.form['username']))
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error  = None
		user = db.execute('select * from user where username = ?', (username, )).fetchone()

		if user is None:
			error = 'incorrect username'
		elif not check_password_hash(user['password'], password):
			# hashes the submitted password in the same way as the stored hash and securely compares them
			error = 'incorrect password'

		if error is None:
			# session is a dict that stores data across requests. 
			session.clear()
			session['user_id'] = user['id']
			logging.debug("login successfully, username:{}, redirect to url_for('index'):{}".format(username, url_for('index')))
			return redirect(url_for('index'))

		flash(error)

	return render_template('auth/login.html')


# register a function to run before the view function, NO MATTER WHAT URL is requested.
@bp.before_app_request
def load_logged_in_user():
	# user_id = session.get('id') # !!!! wrong here! will cause user_id is None forever!
	user_id = session.get('user_id')
	logging.debug("before_app_request, user_id:{}".format(user_id))

	# g.user is ONLY available for the lifetime of THIS REQUEST.
	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute('select * from user where id = ?', (user_id, )).fetchone()


@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))


# Below is a decorator(you can see only two def below)! not a decorator factory(three def)!!
# This decorator returns a new view function that wraps the original view
#  it’s applied to check whether the user is logged in before each view is applied
def login_required(view):
	# functools.wraps : it takes a function (view) in , and copy the information(__name__, __doc__, ...) of this function(view)
	# to the function it decorated(i.e new_view)
	@functools.wraps(view)
	def new_view(**kwargs):
		logging.debug("when check login_required, g.user:{}".format(g.user))
		if g.user is None:
			return redirect(url_for('auth.login'))
		return view(**kwargs)

	return new_view
