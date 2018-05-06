import os
from flask import Flask

"""
# How to run this app

export FLASK_APP=flaskr
export FLASK_ENV=dev
flask run
# or publicly visible
flask run --host 0.0.0.0

# What if I want to run two apps simultaneously 

"""

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        # TODO use python3's os.mkdirs
        os.mkdir(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db

    db.init_app(app)

    return app
