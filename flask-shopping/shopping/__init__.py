from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy, model
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
    rests = [
        {'fullname':'restaurant1', 'nickname':'rest1', 'location':'beijing', 'phone':'123445322', 'password':'rest1', 'company_names':'company1,company2,company3'},
        {'fullname':'restaurant2', 'nickname':'rest2', 'location':'shanghai', 'phone':'423442322', 'password': 'rest2', 'company_names':'company1'}
    ]

    foods = [
        {'name':'food1', 'price': 1.3, 'rest_name': 'rest1'},
        {'name':'food2', 'price': 2, 'rest_name': 'rest1'},
        {'name':'food1', 'price': 2.3, 'rest_name': 'rest2'},
        {'name':'food4', 'price': 5, 'rest_name': 'rest2'}
    ]

    companys = [
        {'name': 'comp1', 'rest_names':'rest1,rest2'},
        {'name': 'comp2', 'rest_names':'rest2'}
    ]

    for r in rests:
        rest = models.Restaurant(fullname=r['fullname'], nickname=r['nickname'], location=r['location'], phone=r['phone'], password= r['password'], company_names = r['company_names'])
        db.session.add(rest)
    
    for f in foods:
        food = models.Food(name=f['name'], rest_name=f['rest_name'], price=f['price'])
        db.session.add(food)
    
    for c in companys:
        comp = models.Company(name = c['name'], rest_names = c['rest_names'])
        db.session.add(comp)

    db.session.commit()
    click.echo("generated fake data.")


@app.cli.command()
def querydb():
    '''
    query database data
    '''
    print(models.Restaurant.query.all())
    print(models.Food.query.all())
    print(models.Company.query.all())
        
    

