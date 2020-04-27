# coding=utf-8

import os
from flask import Flask

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config = True)
    module = __import__(__name__)
    path = os.path.abspath(module.__file__)
    print("in flaskr/__init__.py, __name__:{}, module:{}, module abspath is {}".format(__name__, module, path))

    # set default settings for the app
    app.config.from_mapping(SECRET_KEY = 'dev', \
            DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'))
    print("app.instance_path:", app.instance_path)
    
    # reload the default settings for app from config.py or test_config
    if test_config is None:
        os.system("cat config.py")
        app.config.from_pyfile('config.py', silent = True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the view directly into the app
    @app.route('/hello')
    def hello():
        return "Hello, world!"

    from . import db 
    db.init_app(app)

    # load and register the blueprint for authorization
    from . import auth 
    app.register_blueprint(auth.bp)

    # load and register blueprint for blog manipulation
    from . import blog 
    app.register_blueprint(blog.bp)
    # ???
    app.add_url_rule('/', endpoint = 'index')

    
    return app
    
