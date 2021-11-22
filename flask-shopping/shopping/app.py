from shopping import app, db
from shopping.models import Seller, Buyer, Good 
from flask import render_template


@app.route('/hello')
def homepage():
    goods = Good.query.all()
    return render_template('homepage.html', goods = goods, username = None)

# @app.route('/register')
# def register():
#     # if method == post:
#     #     username = 
#     #     password = 
#     #     add_user_to_database()
#     #     goods = Good.query.all()
#     #     return render_template('homepage.html', goods = goods, username = None)

#     return render_template('register.html')