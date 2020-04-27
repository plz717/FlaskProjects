import pytest
from flaskr.db import get_db


def test_index(client, auth):
	response = client.get('/')
	assert b"Log In" in response.data
	assert b"Register" in response.data

	auth.login()
	response = client.get('/')
	assert b"Log Out" in response.data
	assert b"test_title" in response.data
	assert b"by test on 2018-01-01" in response.data
	assert b"test\nbody" in response.data
	assert b'href="/1/update"' in response.data


@pytest.mark.parametrize('path', \
	('/create', '/1/update', '/1/delete', ))
def test_login_required(client, auth, path):
	response = client.post(path) # can change post to get 
	assert response.headers['Location'] == 'http://localhost/auth/login'


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        # this line is very important! or the change will not take effect!!
        db.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post('/1/update').status_code == 403 # can change post to get 
    assert client.post('/1/delete').status_code == 403 # cannot change post to get 
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', ('/2/update', '/2/delete', ))
def test_exists_required(client, auth, path):
	auth.login()
	# 404 not found, why post here instead of get???
	assert client.post(path).status_code == 404


def test_create(app, client, auth):
	auth.login()
	assert client.get('/create').status_code == 200 # OK
	client.post('/create', data = {'title':'created', 'body':''})

	with app.app_context():
		db = get_db()
		count = db.execute('select count(id) from post').fetchone()[0]
		assert count == 2


def test_update(app, client, auth):
	auth.login()
	# why?? since author_id has been changed from 1 to 2, why 200 OK here?		
	assert client.get('/1/update').status_code == 200
	client.post('/1/update', data = {'title':'updated', 'body':''})

	with app.app_context():
		db = get_db()
		title = db.execute('select title from post where id = 1', ).fetchone()[0]
		assert title == 'updated'


@pytest.mark.parametrize('path', ('/create', '/1/update', ))
def test_create_update_validate(client, auth, path):
	auth.login()
	response = client.post(path, data = {'title':'', 'body':''})
	assert b"title is required" in response.data


def test_delete(app, client, auth):
	auth.login()
	response = client.post('/1/delete') # cannot change post to get 
	assert response.headers['Location'] == 'http://localhost/'

	with app.app_context():
		db = get_db()
		post = db.execute('select * from post where id = 1', ).fetchone() 
		assert post is None