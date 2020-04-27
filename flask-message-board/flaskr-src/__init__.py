from flask import Flask 

app = Flask(__name__)
app.secret_key = 'plz'

@app.route('/')
def index():
	return "hello world!"

from .db import init_db_for_app
init_db_for_app(app)


from .auth import auth_bp
app.register_blueprint(auth_bp)