from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
import os


app = Flask(__name__)
app.config.from_envvar('APP_SETTINGS')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



