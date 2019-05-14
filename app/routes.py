"""File containing all endpoints in the app."""
from flask import request, jsonify
from flask_restful import Resource
from app.users import User  # pylint: disable = syntax-error
from app.organizations import Organization
from app.exceptions import InvalidOrganizationName
from app.exceptions import SignedOrganization
from app import app, db, socketio
from app import app
from app.exceptions import InvalidMail, SignedMail
from app.exceptions import InvalidToken, UserNotRegistered
from app.exceptions import InvalidCookie
from app.messages import Message
from flask_socketio import emit


class Index(Resource):
    """home endpoint"""
    @classmethod
    def get(cls):
        """get mmethod"""
        app.logger.info('home visited')  # pylint: disable=no-member


class Android(Resource):
    """android endpoint"""
    @classmethod
    def get(cls):
        """get mmethod"""
        return "Hello, android"


class AllUsers(Resource):
    """all users endpoint"""
    @classmethod
    def get(cls):
        """get mmethod"""
        try:
            users = User.query.all()
            return jsonify([e.serialize() for e in users])
        except Exception as exception:  # pylint: disable = broad-except
            return str(exception)


class Register(Resource):
    """add users endpoint"""
    @classmethod
    def post(cls):
        """post method"""
        content = request.get_json()
        name = content['name']
        mail = content['mail']
        try:
            User.add_user(name, mail)
            response = jsonify({'message': 'User added'})
            response.status_code = 200
        except (InvalidMail, SignedMail, UserNotRegistered) as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response


class Login(Resource):
    """login users endpoint"""
    @classmethod
    def post(cls):
        """post method"""
        content = request.get_json()
        token = content['token']
        try:
            cookie, expires = User.login_user(token)
            response = jsonify({'message': 'User logged'})
            response.set_cookie(
                'session', cookie, expires=expires, httponly=True, secure=True)
            response.status_code = 200
        except InvalidToken as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response


class Logout(Resource):
    """logout users endpoint"""
    @classmethod
    def post(cls):
        """post method"""
        session_cookie = request.cookies.get('session')
        try:
            User.get_user_claims(session_cookie)
            response = jsonify({'message': 'User Logged out'})
            response.set_cookie('session', expires=0)
            response.status_code = 200
        except InvalidCookie as error:
            response.data = jsonify({'message': error.message})
            response.status_code = error.code

        return response


class DeleteUsers(Resource):
    """delete users endpoint"""
    @classmethod
    def delete(cls):
        """delete method"""
        User.delete_all()


class DeleteUser(Resource):
    """delete users endpoint"""
    @classmethod
    def delete(cls):
        """delete method"""
        content = request.get_json()
        mail = content['mail']
        User.delete_user_with_mail(mail)

class CreateOrganization(Resource):
    """create new orga"""
    @classmethod
    def post(cls):
        """post method"""
        content = request.get_json()
        org_name = content['org_name']
        session_cookie = request.cookies.get('session')
        try:
            creator_user_id = User.get_user_with_cookie(session_cookie)
            orga = Organization.add_orga(org_name, creator_user_id)
            data = {'id': orga.id,
                    'message': 'orga added'
                    }

            create_organization_specific_table(org_name)

            response = jsonify(data)
            response.status_code = 200
        except(InvalidOrganizationName, SignedOrganization) as error:
            response = jsonify(error.message)
            response.status_code = error.code
        except InvalidCookie:
            return flask.redirect('/login')
        return response

def save(msg, user_id):
    content = json.loads(msg)

    organization = content['organization']
    channel = content['channel']
    dm_dest = content['dm_dest']
    author_id = user_id
    body = content['body']
    Message.add_message(organization, channel, dm_dest, author_id, body)

    if organization:
        deliver_msg(body, organization, channel, author_id)
    else:
        deliver_dm(body, dm_dest, author_id)

def deliver_dm(msg_body, dm_dest, author_id):
    """ if user is online, the msg gets delivered. """
    author_name = User.get_user_by_id(author_id).name

    d = {'msg_body':msg_body,
            'author_name':author_name}

    if User.is_online(dm_dest):
        sid = User.get_user_by_id(dm_dest).sid
        emit('dm', d, room=sid)

def deliver_msg(msg_body, org_name, channel, author_id):
    """ deliver msg to connected users. """

    org_id = Organization.get_organization_by_name(org_name).id
    author_name = User.get_user_by_id(author_id).name

    d = {'msg_body':msg_body,
            'organization':org_name,
            'channel':channel,
            'author_name':author_name}

    users = Channel.get_users_in_channel(channel_name, org_id)

    for user in users:
        if User.is_online(user):
            sid = User.get_user_by_id(user).sid
            emit('message', d, room=sid)

@socketio.on('message')
def handleMessage(msg):
    user = User.get_user_by_sid(sid)
    app.logger.info('Received msg: ' + msg)
    save_msg(msg, user.id)
    deliver_msg(msg)

@socketio.on('connect')
def handle_message():
#    session_cookie = request.cookies.get('session')
#    user_id = User.get_user_with_cookie(session_cookie)
#    user = User.get_user_by_id(user_id)
    app.logger.info('new connnectionn: sid ' + request.sid + ' connected.')

@socketio.on('identification')
def identyfy_connected_user(mail):
    sid = request.sid
    user = User.get_user_by_mail(mail)
    user.udpate_sid(sid)
    app.logger.info('identified user ' + mail + ' with sid ' + sid)

@socketio.on('disconnect')
def disconnect_socket_user():
    sid = request.sid
    user = User.get_user_by_sid(sid)
    user.udpate_sid(' ')
    app.logger.info('user with sid ' + sid + ' disconnected.')
