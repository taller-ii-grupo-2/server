"""File containing all endpoints in the app."""
import json
from flask import request, jsonify
from flask_restful import Resource
from flask_socketio import emit
import sqlalchemy.exc as sql
from app.users import User  # pylint: disable = syntax-error
from app.organizations import Organization
from app.exceptions import InvalidOrganizationName
from app.exceptions import SignedOrganization
from app import app, socketio
from app.exceptions import InvalidMail, SignedMail
from app.exceptions import InvalidToken, UserNotRegistered
from app.exceptions import InvalidCookie, InvalidUser
from app.exceptions import UserIsAlredyInOrganization
from app.exceptions import InvalidOrganization
from app.exceptions import AlreadyCreatedChannel
from app.exceptions import UserNotInOrganization, InvalidChannelName
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
            return jsonify([e.name for e in users])
        except Exception as exception:  # pylint: disable = broad-except
            return str(exception)


class Users(Resource):
    """add users endpoint"""
    @classmethod
    def post(cls):
        """post method"""
        content = request.get_json()
        user_name = content['username']
        name = content['name']
        surname = content['surname']
        mail = content['mail']
        latitude = content['latitude']
        longitude = content['longitude']
        url = content['urlImageProfile']
        try:
            User.add_user(user_name, name, surname, mail, latitude,
                          longitude, url)
            response = jsonify({'message': 'User added'})
            response.status_code = 200
        except (InvalidMail, SignedMail, UserNotRegistered) as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response

    @classmethod
    def put(cls):
        """post method"""
        content = request.get_json()
        user_name = content['username']
        name = content['name']
        surname = content['surname']
        url = content['urlImageProfile']
        session_cookie = request.cookies.get('session')
        try:
            user = User.get_user_with_cookie(session_cookie)
            user.change(user_name, name, surname, url)
            response = jsonify({'message': 'User changed'})
            response.status_code = 200
        except (InvalidMail, SignedMail, UserNotRegistered) as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response

    @classmethod
    def get(cls):
        """post method"""
        session_cookie = request.cookies.get('session')
        try:
            user = User.get_user_with_cookie(session_cookie)
            response = jsonify(user.serialize())
            response.status_code = 200
        except InvalidCookie as error:
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
            response = jsonify({'message': error.message})
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


class Organizations(Resource):
    """create new orga"""
    @classmethod
    def post(cls):
        # pylint: disable = W0702
        """post method"""
        # pylint: disable=no-member
        app.logger.info('in orga creation')
        content = request.get_json(force=True)
        app.logger.info('Received content: ' + str(content))
        org_name = content['name']
        description = content['description']
        welcome_message = content['welcomMsg']
        url_image = content['urlImage']

        app.logger.info('org_name: ' + str(org_name))
        app.logger.info('description: ' + str(description))
        app.logger.info('welcome_message: ' + str(welcome_message))
        app.logger.info('url_image: ' + str(url_image))
        session_cookie = request.cookies.get('session')
        # pylint: disable=no-member
        try:
            creator_user = User.get_user_with_cookie(session_cookie)
            app.logger.info('creator_user_id: ' + str(creator_user))
            Organization.create(org_name, url_image, creator_user,
                                description, welcome_message)
            data = {'message': 'orga added'}
            response = jsonify(data)
            response.status_code = 200
        except(InvalidOrganizationName, SignedOrganization,
               InvalidCookie) as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        except:  # noqa: E722
            data = {'message': 'sql data error'}
            response = jsonify(data)
            response.status_code = 500
        return response


class UserOrganizations(Resource):
    """ orrganization from users"""
    @classmethod
    def get(cls):
        """ get users orgas """
        # pylint: disable=no-member
        app.logger.info('in users organizations')
        session_cookie = request.cookies.get('session')
        # pylint: enable=no-member
        try:
            user = User.get_user_with_cookie(session_cookie)
            orgas = user.get_organizations()

            list_of_orgas = []
            for orga in orgas:
                orga_dict = {'name': orga['name'], 'urlImage': orga['url']}
                list_of_orgas.append(orga_dict)

            response = jsonify(list_of_orgas)
            response.status_code = 200
            # pylint: disable=no-member
            app.logger.info('sending orgas: ' + str(response.data))
            # pylint: enable=no-member
        except InvalidCookie as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response


class OrganizationMembers(Resource):
    """ organization's members """
    @classmethod
    def put(cls):
        """add new member"""
        content = request.get_json()
        org_name = content['org_name']
        mail_of_user_to_add = content['mail_of_user_to_add']
        session_cookie = request.cookies.get('session')
        try:
            User.get_user_with_cookie(session_cookie)
            user_to_add = User.get_user_by_mail(mail_of_user_to_add)
            orga = Organization.get_organization_by_name(org_name)
            orga.add_user(user_to_add)

            data = {'message': 'user added'}

            response = jsonify(data)
            response.status_code = 200
        except(UserIsAlredyInOrganization, InvalidOrganization,
               InvalidCookie, InvalidUser) as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response


class OrganizationMembersLocations(Resource):
    """ locations of the members """
    @classmethod
    def get(cls, org_name):
        """get location of the members"""

        session_cookie = request.cookies.get('session')
        try:
            User.get_user_with_cookie(session_cookie)
            orga = Organization.get_organization_by_name(org_name)
            users = orga.get_users_location()
            response = jsonify(users)
            response.status_code = 200
        except(InvalidCookie, InvalidOrganization) as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response


class UserOrganizationsChannels(Resource):
    """ channels in organization from user """
    @classmethod
    def get(cls, org_name):
        """get channels in organization where the user is"""
        # pylint: disable=no-member
        app.logger.info('in user organization channels')
        session_cookie = request.cookies.get('session')
        try:
            User.get_user_with_cookie(session_cookie)
            orga = Organization.get_organization_by_name(org_name)
            channel_names = []
            member_mails = []

            for channel in orga.channels:
                channel_names.append(channel.name)

            for member in orga.users:
                member_mails.append(member.mail)

            data = {'description': orga.description,
                    'welcomMsg': orga.welcome_message,
                    'urlImage': orga.url,
                    'channels': channel_names,
                    'members': member_mails}
            response = jsonify(data)
            response.status_code = 200
            app.logger.info('sending data: ' + str(response.data))
        # pylint: enable=no-member
        except(InvalidCookie, InvalidOrganization) as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response


class Channels(Resource):
    """ manage channels in organizations """
    @classmethod
    def post(cls):
        """ create channel in organization """
        content = request.get_json()
        org_name = content['nameOrga']
        channel_name = content['channel_name']
        public = content['public']
        description = content['desc']
        session_cookie = request.cookies.get('session')
        try:
            user = User.get_user_with_cookie(session_cookie)
            orga = Organization.get_organization_by_name(org_name)
            orga.create_channel(channel_name, public, user,
                                description, 'wm')
            data = {'message': 'user added'}
            response = jsonify(data)
            response.status_code = 200
        except(InvalidCookie, AlreadyCreatedChannel,
               UserNotInOrganization, sql.DataError,
               InvalidChannelName) as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response


class Messages(Resource):
    """ manage general msgs (not private dms) """
    @classmethod
    def get(cls, orga_name, channel_name):
        """get msgs of specified orga/channel"""
        retrieved_msgs = Message.get_channel_messages(orga_name, channel_name)
        msgs_to_send = []
        for msg in retrieved_msgs:
            author_mail = User.get_user_by_id(msg.author_id).mail
            msgs_to_send.append({'timestamp': msg.timestamp,
                                 'author_mail': author_mail,
                                 'body': msg.body})
        return msgs_to_send


class PrivateMessages(Resource):
    """ manage private msgs """
    @classmethod
    def get(cls, orga_name, dm_dest_mail):
        """get private  msgs """
        session_cookie = request.cookies.get('session')
        asker_mail = User.get_user_with_cookie(session_cookie).mail

        retrieved_msgs = Message.get_dms(orga_name, dm_dest_mail, asker_mail)
        msgs_to_send = []
        for msg in retrieved_msgs:
            msgs_to_send.append({'timestamp': msg.timestamp,
                                 'author_mail': msg.author_mail,
                                 'body': msg.body})
        return msgs_to_send


def save_msg(msg, user_id):
    """ save received msg to db """
    content = json.loads(msg)

    organization = content['organization']
    channel = content['channel']
    dm_dest = content['dm_dest']
    author_mail = User.get_user_by_id(user_id).mail
    body = content['body']
    msg = Message.add_message(organization,
                              channel, dm_dest, author_mail, body)

    if channel:
        deliver_msg(body, organization, channel, author_mail, msg.timestamp)
    else:
        deliver_dm(body, dm_dest, author_mail, msg.timestamp)


def deliver_dm(msg_body, dm_dest, author_mail, timestamp):
    """ if user is online, the msg gets delivered. """

    msg_dict = {'msg_body': msg_body,
                'author_mail': author_mail,
                'timestamp': str(timestamp)}

    if User.is_online(dm_dest):
        sid = User.get_user_by_mail(dm_dest).sid
        emit('dm', msg_dict, room=sid)


def deliver_msg(msg_body, org_name, channel_name, author_mail, timestamp):
    """ deliver msg to connected users. """

    org_id = Organization.get_organization_by_name(org_name).id

    msg_dict = {'msg_body': msg_body,
                'organization': org_name,
                'channel': channel_name,
                'author_mail': author_mail,
                'timestamp': str(timestamp)}

    users = Channel.get_users_in_channel(channel_name, org_id)

    for user in users:
        if User.is_online(user.mail):
            sid = User.get_user_by_id(user.id).sid
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
    # pylint: disable=no-member
    sid = request.sid
    user = User.get_user_by_sid(sid)  # pylint: disable=no-member
    app.logger.info('user disconnected: ' + sid + ", " + user.mail)
    user.udpate_sid(' ')
