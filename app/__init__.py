import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

ma = Marshmallow(app)
api = Api(app)
CORS(app)

from app import models, forms, routes, apies, dnevnik, workfiles