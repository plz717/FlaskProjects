from flask import Flask 

app = Flask(__name__)
app.secret_key = 'plz'

# @app.route('/')
# def hello():
# 	return "hello world!"

from .db import init_db_for_app
init_db_for_app(app)


from .auth import auth_bp
app.register_blueprint(auth_bp)

from .message import msg_bp
app.register_blueprint(msg_bp)
app.add_url_rule('/', endpoint = 'index')
