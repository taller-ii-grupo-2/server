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
from flask_jwt_extended import JWTManager


cred = credentials.Certificate('hypechatapp.json')
default_app = firebase_admin.initialize_app(cred)

app = Flask(__name__)
app.config.from_object(Config)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)
db = SQLAlchemy(app)
api = Api(app)
socketio = SocketIO(app)

logging.Formatter.converter = time.localtime
logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        # filename='log/basic.log',
        level=logging.DEBUG)

from app import routes, users  # noqa: E402, F401

# endpoints de prueba
api.add_resource(routes.Index, '/')
api.add_resource(routes.Android, '/android')
api.add_resource(routes.AllUsers, '/users/all')
# hasta aqui endpoints de prueba

api.add_resource(routes.OrganizationMembers, '/organizations/members')
api.add_resource(routes.OrganizationChannels, '/organizations/channels')
api.add_resource(routes.Profile, '/profile/<mail>')
api.add_resource(routes.OrganizationMembersLocations,
                 '/organizations/<org_name>/members/locations')
api.add_resource(routes.Organizations, '/organizations')
api.add_resource(routes.OrganizationUsersRoles, '/type/<name_orga>')
api.add_resource(routes.UserOrganizations, '/user/organizations')
api.add_resource(routes.AdminLogin, '/adminlogin')
api.add_resource(routes.UserOrganizationsChannels,
                 '/user/organizations/<org_name>/channels')
# api.add_resource(routes.ShowOrganization, '/myorganizations')
api.add_resource(routes.Users, '/users')
api.add_resource(routes.DeleteUsers, '/delete')
api.add_resource(routes.Login, '/login')
api.add_resource(routes.Logout, '/logout')
api.add_resource(routes.DeleteUser, '/deleteone')
api.add_resource(routes.Channels, '/channels')
api.add_resource(routes.UsersFromChannels, '/channels/users')
api.add_resource(routes.Messages, '/messages/<orga_name>/<channel_name>')
api.add_resource(routes.PrivateMessages,
                 '/messages/<orga_name>/dms/<dm_dest_mail>')
api.add_resource(routes.AdminSeeUsers, '/users/total')
api.add_resource(routes.InvalidWords, '/organizations/invalidwords')
api.add_resource(routes.AdminBots, '/admin/bots')
api.add_resource(routes.ChannelInfoForBot,
                 '/bots/<organization_name>/<channel_name>')
api.add_resource(routes.UsersInfoForBot, '/bots/users/<user_mail>')

app.logger.info('in main')
