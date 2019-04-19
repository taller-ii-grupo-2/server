# pylint: skip-file
from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
db = SQLAlchemy(app)
api = Api(app)

from app import routes, users  # noqa: E402, F401

api.add_resource(routes.Index, '/')
api.add_resource(routes.Android, '/android')
api.add_resource(routes.AllUsers, '/users/all')
api.add_resource(routes.AddUsers, '/register')
