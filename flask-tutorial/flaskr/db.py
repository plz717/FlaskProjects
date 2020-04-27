# coding=utf-8

import sqlite3

import click
from flask import current_app,  g
from flask.cli import with_appcontext


def get_db():
    print("in get_db, 'db' is in g:{}".format('db' in g))
    # g is a thread local and is per-request
    if 'db' not in g:
        print("current_app.config['DATABASE']:", current_app.config['DATABASE'])
        g.db = sqlite3.connect(current_app.config['DATABASE'], \
                               detect_types = sqlite3.PARSE_DECLTYPES)
    g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e = None):
    print("in close_db, e:", e)
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """clear the existing data and create new tables"""
    init_db()
    click.echo("initialized the database.")


def init_app(app):
    # tell flask to call close_db when teardown_app_context
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

