# pylint: skip-file
from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_socketio import SocketIO
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

# endpoints de prueba
api.add_resource(routes.Index, '/')
api.add_resource(routes.Android, '/android')
api.add_resource(routes.AllUsers, '/users/all')
# hasta aqui endpoints de prueba

api.add_resource(routes.OrganizationMembers, '/organizations/members')
api.add_resource(routes.OrganizationMembersLocations,
                 '/organizations/members/locations')
api.add_resource(routes.Organizations, '/organizations')
api.add_resource(routes.UserOrganizations, '/user/organizations')
api.add_resource(routes.UserOrganizationsChannels,
                 '/user/organizations/channels')
api.add_resource(routes.Organizations, '/organizations')
# api.add_resource(routes.ShowOrganization, '/myorganizations')
api.add_resource(routes.Users, '/users')
api.add_resource(routes.DeleteUsers, '/delete')
api.add_resource(routes.Login, '/login')
api.add_resource(routes.Logout, '/logout')
api.add_resource(routes.DeleteUser, '/deleteone')


app.logger.info('in main')
