from flask import Blueprint, request, render_template, url_for, redirect, flash, g, session
from .db import get_db


msg_bp = Blueprint('msg', __name__)


@msg_bp.route('/', methods = ('GET', 'POST'))
def index():
	# get post data
	db = get_db()
	try:
		posts = db.execute('select * from post_table').fetchall()
	except:
		print("post_table not exists.")
		posts = None

	# if request.form['method'] == 'POST':
	# 	# blabla
	g.user = session['username']
	print("in index, g.user :", g.user)
	return render_template('message/index.html', data = posts)


@msg_bp.route('/create', methods = ('GET', 'POST'))
def create():
	print("in create, g.user:", g.user)
	if g.user is None:
		return redirect(url_for('auth/login'))

	if request.form['method'] == 'POST':
		title = request.form['title']
		body = request.form['body']
		time = '20200428'

		error = None
		if title is None or title == '':
			error = "title is required!"
		elif body is None or body == '':
			error = 'body is required!'
		else:
			# no error, then insert the data to post table
			db = get_db()
			db.execute('insert into post_table values (?, ?, ?, ?)', (title, body, time, g.user))
			db.commit()
			return redirect(url_for('index'))

	flash(error)
	return render_template('message/create.html')

