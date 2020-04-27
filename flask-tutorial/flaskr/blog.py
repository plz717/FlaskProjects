from flask import Blueprint, flash, g, redirect, render_template, request, url_for, session
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import logging
logging.basicConfig(level = logging.DEBUG)


bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
	user_id = session.get('user_id')
	logging.debug("in index, user_id:{}, g.user:{}".format(user_id, g.user))
	db = get_db()
	posts = db.execute('select p.id, title, body, created, author_id, u.username \
						from post p join user u on p.author_id = u.id \
						order by created desc').fetchall()
	return render_template('blog/index.html', posts = posts)


@bp.route('/create', methods = ('GET', 'POST'))
@login_required
def create():
	if request.method == 'POST':
		title = request.form['title']
		body = request.form['body']
		error = None

		if not title:
			error = "title is required."

		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute('insert into post (title, body, author_id) values (?, ?, ?)', (title, body, g.user['id']))
			db.commit()
			return redirect(url_for('blog.index'))

	return render_template('blog/create.html')


def get_post(id, check_author = True):
	all_post = get_db().execute('select p.id as id, title, body, created, author_id, u.username \
							from post p join user u on p.author_id = u.id', )
	logging.debug("="*15)
	logging.debug("all posts ids:")
	for row in all_post:
		print("post id:{}".format(row['id']))
	post = get_db().execute('select p.id, title, body, created, author_id, u.username \
							from post p join user u on p.author_id = u.id\
							where p.id = ?', (id, )).fetchone()

	if post is None:
		abort(404, "Post id {} doesn't exists.".format(id))
	else:
		logging.debug("post id {} exists, post author_id:{}, user_id:{}".format(post['id'], post['author_id'], g.user['id']))

	if check_author and post['author_id'] != g.user['id']:
		abort(403, "Only author of the article can update!")
	return post


@bp.route('/<int:id>/update', methods = ('GET', 'POST'))
@login_required
def update(id):
	post = get_post(id, check_author = True)
	logging.debug("in update fun, post['id']:{}".format(post['id']))

	if request.method == 'POST':
		title = request.form['title']
		body = request.form['body']
		error = None

		if not title:
			error = "title is required."

		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute('update post set title = ?, body = ? where id = ?', (title, body, id))
			db.commit()
			return redirect(url_for('blog.index'))

	return render_template('blog/update.html', post = post)


@bp.route('/<int:id>/delete', methods = ('GET', 'POST'))
@login_required
def delete(id):
	get_post(id)
	db = get_db()
	db.execute('delete from post where id = ?', (id, ))
	db.commit()
	return redirect(url_for('blog.index'))



