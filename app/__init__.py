# pylint: skip-file
from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_socketio import SocketIO
import logging
import time
import firebase_admin
from firebase_admin import credentials, messaging

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
        # filename='log/basic.log',
        level=logging.DEBUG)

from app import routes, users  # noqa: E402, F401

# endpoints de prueba
api.add_resource(routes.Index, '/')
api.add_resource(routes.Android, '/android')
api.add_resource(routes.AllUsers, '/users/all')
# hasta aqui endpoints de prueba

api.add_resource(routes.OrganizationMembers, '/organizations/members')
api.add_resource(routes.OrganizationMembersLocations,
                 '/organizations/<org_name>/members/locations')
api.add_resource(routes.Organizations, '/organizations')
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


app.logger.info('in main')
# messaging.AndroidNotification(title="title notif", body="notif body")
# This registration token comes from the client FCM SDKs.
registration_token = "dtDcV2El9wo:APA91bEYGVw2onreMsqlKOoowctQWD3VMVrrVgUzwNSYZSnt_BjQ0rf-Cr5NXakKpkfAMLpzQcd8VamgVS5wlvlA73bGnD74bcg4B936Nhcme1kx7kHN-uhad_RtrljvH0AovIHEhw4G"

# See documentation on defining a message payload.
message = messaging.Message(
        notification = messaging.Notification(title='title', body='body'),
        token=registration_token,)

# Send a message to the device corresponding to the provided
# registration token.
response = messaging.send(message)
# Response is a message ID string.
print('Successfully sent message:', response)

