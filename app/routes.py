"""File containing all endpoints in the app."""
import json
from flask import request, jsonify, redirect
from flask_restful import Resource
from flask_socketio import emit
from app.users import User  # pylint: disable = syntax-error
from app.organizations import Organization
from app.exceptions import InvalidOrganizationName
from app.exceptions import SignedOrganization
from app import app, socketio
from app.exceptions import InvalidMail, SignedMail
from app.exceptions import InvalidToken, UserNotRegistered
from app.exceptions import InvalidCookie
from app.exceptions import UserIsAlredyInOrganization, UserIsNotAdmin
from app.messages import Message
from app.channels import Channel


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
        org_name = content['name']
        description = content['description']
        welcome_message = content['welcome_message']
        url_image = content['urlImage']

        session_cookie = request.cookies.get('session')
        try:
            creator_user_id = User.get_user_with_cookie(session_cookie)
            orga = Organization.create(org_name, url_image, creator_user_id,
                                       description, welcome_message)
            data = {'id': orga.id,
                    'message': 'orga added'
                    }

            response = jsonify(data)
            response.status_code = 200
        except(InvalidOrganizationName, SignedOrganization) as error:
            response = jsonify(error.message)
            response.status_code = error.code
        except InvalidCookie:
            return redirect('/login')
        return response


class OrganizationMembers(Resource):
    """ organization's members """
    @classmethod
    def put(cls):
        """add new member"""
        content = request.get_json()
        org_name = content['org_name']
        mail_of_user_to_add = content['mail']
        session_cookie = request.cookies.get('session')
        try:
            adder_user = User.get_user_with_cookie(session_cookie)
            user_to_add = User.get_user_by_mail(mail_of_user_to_add)
            orga = Organization.get_organization_by_name(org_name)
            orga.add_user(adder_user, user_to_add)

            data = {'message': 'user added'}

            response = jsonify(data)
            response.status_code = 200
        except(UserIsAlredyInOrganization) as error:
            response = jsonify(error.message)
            response.status_code = error.code
        except UserIsNotAdmin as error:
            response = jsonify(error.message)
            response.status_code = error.code
        except InvalidCookie:
            return redirect('/login')
        return response


class Organizations(Resource):
    """ manage orga """
    @classmethod
    def get(cls):
        """ get users orgas """
        session_cookie = request.cookies.get('session')
        try:
            user = User.get_user_with_cookie(session_cookie)
            orgas = user.get_organizations()

            list_of_orgas = []
            for orga in orgas:
                current_orga_dict = {}
                current_orga_dict['name'] = orga.name
                current_orga_dict['urlImage'] = orga.url
                list_of_orgas.append(current_orga_dict)

            response = jsonify(list_of_orgas)
            response.status_code = 200
        except InvalidCookie:
            return redirect('/login')
        return response


def save_msg(msg, user_id):
    """ save received msg to db """
    content = json.loads(msg)

    organization = content['organization']
    channel = content['channel']
    dm_dest = content['dm_dest']
    author_id = user_id
    body = content['body']
    msg = Message.add_message(organization, channel, dm_dest, author_id, body)

    if organization:
        deliver_msg(body, organization, channel, author_id, msg.timestamp)
    else:
        deliver_dm(body, dm_dest, author_id, msg.timestamp)


def deliver_dm(msg_body, dm_dest, author_id, timestamp):
    """ if user is online, the msg gets delivered. """
    author_name = User.get_user_by_id(author_id).name

    msg_dict = {'msg_body': msg_body,
                'author_name': author_name,
                'timestamp': timestamp}

    if User.is_online(dm_dest):
        sid = User.get_user_by_id(dm_dest).sid
        emit('dm', msg_dict, room=sid)


def deliver_msg(msg_body, org_name, channel_name, author_id, timestamp):
    """ deliver msg to connected users. """

    org_id = Organization.get_organization_by_name(org_name).id
    author_name = User.get_user_by_id(author_id).name

    msg_dict = {'msg_body': msg_body,
                'organization': org_name,
                'channel': channel_name,
                'author_name': author_name,
                'timestamp': timestamp}

    users = Channel.get_users_in_channel(channel_name, org_id)

    for user in users:
        if User.is_online(user):
            sid = User.get_user_by_id(user).sid
            emit('message', msg_dict, room=sid)


@socketio.on('message')
def handle_message(msg):
    """save msg to db and deliver it to connected people"""
    user = User.get_user_by_sid(request.sid)
    app.logger.info('Received msg: ' + msg)  # pylint: disable=no-member
    save_msg(msg, user.id)


@socketio.on('connect')
def handle_new_connection():
    """log new connection"""
    # pylint: disable=no-member
    app.logger.info('new connnectionn: sid ' + request.sid + ' connected.')
    # pylint: enable=no-member


@socketio.on('identification')
def identify_connected_user(mail):
    """match user with sid (session unique id)"""
    # pylint: disable=no-member
    app.logger.info('identifying... mail: ' + mail)
    # pylint: enable=no-member
    sid = request.sid
    user = User.get_user_by_mail(mail)
    user.udpate_sid(sid)
    # pylint: disable=no-member
    app.logger.info('identified user ' + mail + ' with sid ' + sid)
    # pylint: enable=no-member


@socketio.on('disconnect')
def disconnect_socket_user():
    """handle user disconnection"""
    sid = request.sid
    user = User.get_user_by_sid(sid)  # pylint: disable=no-member
    user.udpate_sid(' ')
    # pylint: disable=no-member
    app.logger.info('user with sid ' + sid + ' disconnected.')
    # pylint: enable=no-member
