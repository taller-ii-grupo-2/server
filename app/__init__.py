# pylint: skip-file
from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, send
import logging
import time


app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
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
api.add_resource(routes.AddUsers, '/users/add')
# api.add_resource(routes.CreateOrganization, '/organizations/creation')

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
