# -*- coding: utf-8 -*-

import sqlite3

import pytest
from flaskr.db import get_db


def test_get_close_db(app):
	'''
	Within an application context, get_db should return the same connection each time it’s called. 
	After the context, the connection should be closed.
	'''
	with app.app_context():
		db = get_db()
		assert db is get_db()

	with pytest.raises(sqlite3.ProgrammingError) as e:
		db.execute('select 1')

	assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
	class Recorder(object):
		called = False

	def fake_init_db():
		Recorder.called = True

	# uses Pytest’s monkeypatch fixture to replace the init_db function
	monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
	result = runner.invoke(args = ['init-db'])
	assert	'initialized' in result.output
	assert Recorder.called

