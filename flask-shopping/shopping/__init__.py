from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import click


app = Flask(__name__)
db = SQLAlchemy(app)
app.secret_key = 'plz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')

from shopping import models

@app.cli.command() 
@click.option('--drop', is_flag = True, help = 'create after drop')
def initdb(drop):
    '''
    initialize database
    '''
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("initialized database.")

@app.cli.command()
def fake():
    '''
    generate fake data.
    '''
    goods = [
        {'title': 'a beautiful red dress for young lady.', 'price': 300},
        {'title': 'comfortable blue shoes for old-man', 'price': 204}
    ]
    for g in goods:
        good = models.Good(title = g['title'], price = g['price'])
        db.session.add(good)

    buyers=[
        {'name':'plz', 'password':'plz'},
        {'name':'xcc', 'password':'xcc'}
    ]
    for b in buyers:
        buyer = models.Buyer(name = b['name'], password=b['password'])
        db.session.add(buyer)

    db.session.commit()
    click.echo("generated fake data.")


@app.cli.command()
def querydb():
    '''
    query database data
    '''
    print(models.Good.query.all())
    print(models.Buyer.query.all())
        
    

