import flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os.path

# gives current directory of this file
basedir = os.path.abspath(os.path.dirname(__file__))
# instance of the Flask class
myapp_obj = flask.Flask(__name__)
myapp_obj.config.from_mapping(
    SECRET_KEY = 'it-dont-matter',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

db = SQLAlchemy(myapp_obj)

login = LoginManager(myapp_obj)
login.login_view = 'login'

from myapp import routes, routesUser, models

db.create_all()