# pylint: skip-file
from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, send
import logging
import time
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('hypechatapp.json')
default_app = firebase_admin.initialize_app(cred)

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
api = Api(app)
socketio = SocketIO(app)

logging.Formatter.converter = time.localtime
logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='log/basic.log',
        level=logging.DEBUG)

from app import routes, users  # noqa: E402, F401

api.add_resource(routes.Index, '/')
api.add_resource(routes.Android, '/android')
api.add_resource(routes.AllUsers, '/users/all')
api.add_resource(routes.CreateOrganization, '/organizations/creation')
api.add_resource(routes.Register, '/register')
api.add_resource(routes.DeleteUsers, '/delete')
api.add_resource(routes.Login, '/login')
api.add_resource(routes.Logout, '/logout')
api.add_resource(routes.DeleteUser, '/deleteone')


app.logger.info('in main')


@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    app.logger.info('broadcasting received msg: ' + msg)
    send(msg, broadcast=True)


@socketio.on('connect')
def handle_message():
    app.logger.info('new connnectionn')
#    print('received message: ' + message)

# @socketio.on('message')
# def handle_message(msg):
#     app.logger.info('broadcasting received msg: ' + msg)
#     send(msg, broadcast = True)

# @socketio.on_error()        # Handles the default namespace
# def error_handler(e):
#     app.logger.info('error occurred: ' + e)

