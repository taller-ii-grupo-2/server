"""File containing all endpoints in the app."""
import json
from flask import request, jsonify
from flask_restful import Resource
from flask_socketio import emit
import sqlalchemy.exc as sql
from flask_jwt_extended import jwt_required
from firebase_admin import messaging
import requests

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
from app.exceptions import AlreadyCreatedChannel, UserIsNotCreator
from app.exceptions import UserNotInOrganization, InvalidChannelName
from app.exceptions import InvalidChannel, UserIsAlredyInChannel
from app.exceptions import NotAdminWeb, UserIsCreator, UserIsNotAdmin
from app.admins import Admin
from app.messages import Message
from app.channels import Channel
from app.fb_user import FbUser, URL
from app.bots import Bot


class Index(Resource):
    """home endpoint"""
    @classmethod
    def get(cls):
        """get mmethod"""
        app.logger.info('home visited')  # pylint: disable=no-member
        return "get received"

    @classmethod
    def post(cls):
        """post mmethod"""
        # pylint: disable=no-member
        app.logger.info('home visited by post method')

        return "post received"


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


class Profile(Resource):
    """ manage users profiles """
    @classmethod
    def get(cls, mail):
        """ get users profiles"""
        session_cookie = request.cookies.get('session')
        try:
            User.get_user_with_cookie(session_cookie)
            user = User.get_user_by_mail(mail)
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
        FbUser.remove_user(mail)
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

    @classmethod
    def delete(cls):
        """ delete orga"""
        content = request.get_json()
        org_name = content['nameOrga']
        session_cookie = request.cookies.get('session')
        try:
            user = User.get_user_with_cookie(session_cookie)
            user.delete_orga(org_name)
            data = {'message': 'orga deleted'}

            response = jsonify(data)
            response.status_code = 200
        except (InvalidCookie, UserIsNotCreator) as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response


class OrganizationUsersRoles(Resource):
    """ manage type of users in orga """
    @classmethod
    def get(cls, name_orga):
        """ get all users with types """
        session_cookie = request.cookies.get('session')
        try:
            User.get_user_with_cookie(session_cookie)
            orga = Organization.get_organization_by_name(name_orga)
            response = jsonify(orga.get_users_roles())
            response.status_code = 200
        except InvalidCookie as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response

    @classmethod
    def put(cls, name_orga):
        """ update role of the user in orga """
        content = request.get_json()
        mail = content['mail']
        role = content['type']
        session_cookie = request.cookies.get('session')
        try:
            user = User.get_user_with_cookie(session_cookie)
            user_to_update = User.get_user_by_mail(mail)
            orga = Organization.get_organization_by_name(name_orga)
            orga.update_user(user, user_to_update, role)
            data = {'message': 'user updated'}

            response = jsonify(data)
            response.status_code = 200
        except InvalidCookie as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response


class OrganizationChannels(Resource):
    """ manage channels of organizations """
    @classmethod
    def delete(cls):
        """ delete channel from orga"""
        content = request.get_json()
        org_name = content['nameOrga']
        name_channel = content['name_channel']
        session_cookie = request.cookies.get('session')
        try:
            User.get_user_with_cookie(session_cookie)
            orga = Organization.get_organization_by_name(org_name)
            Channel.delete_channel(name_channel, orga.id)
            data = {'message': 'channel deleted'}

            response = jsonify(data)
            response.status_code = 200
        except InvalidCookie as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
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
    def post(cls):
        """invite new member"""
        content = request.get_json()
        org_name = content['org_name']
        mail_of_user_to_add = content['mail_of_user_to_add']
        session_cookie = request.cookies.get('session')
        try:
            user_inviting = User.get_user_with_cookie(session_cookie)
            user_to_add = User.get_user_by_mail(mail_of_user_to_add)
            orga = Organization.get_organization_by_name(org_name)
            orga.invite_user(user_to_add, user_inviting)
            orga.add_user(user_to_add)

            data = {'message': 'user invited'}

            response = jsonify(data)
            response.status_code = 200
        except(UserIsAlredyInOrganization, InvalidOrganization,
               InvalidCookie, InvalidUser) as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response

    @classmethod
    def put(cls):
        """add new member"""
        content = request.get_json()
        org_name = content['org_name']
        session_cookie = request.cookies.get('session')
        try:
            user_to_add = User.get_user_with_cookie(session_cookie)
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

    @classmethod
    def delete(cls):
        """ delete member from orga"""
        content = request.get_json()
        org_name = content['nameOrga']
        mail = content['mail']
        session_cookie = request.cookies.get('session')
        try:
            user = User.get_user_with_cookie(session_cookie)
            user_to_remove = User.get_user_by_mail(mail)
            orga = Organization.get_organization_by_name(org_name)
            user.remove_user_from_orga(orga, user_to_remove)
            data = {'message': 'user deleted'}

            response = jsonify(data)
            response.status_code = 200
        except(UserIsCreator, UserIsNotAdmin,
               InvalidCookie) as error:
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
            user = User.get_user_with_cookie(session_cookie)
            orga = Organization.get_organization_by_name(org_name)
            channel_names = orga.get_channels_with_user(user.id)
            member_mails = []

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
        private = content['private']
        description = content['desc']
        session_cookie = request.cookies.get('session')
        try:
            user = User.get_user_with_cookie(session_cookie)
            orga = Organization.get_organization_by_name(org_name)
            orga.create_channel(channel_name, private, user,
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


class UsersFromChannels(Resource):
    """ manage users in channels """
    @classmethod
    def post(cls):
        """ add user to channel """
        content = request.get_json()
        org_name = content['nameOrga']
        channel_name = content['channel_name']
        mail = content['user_mail']
        session_cookie = request.cookies.get('session')
        try:
            User.get_user_with_cookie(session_cookie)
            orga = Organization.get_organization_by_name(org_name)
            user = User.get_user_by_mail(mail)
            orga.add_user_to_channel(user, channel_name)
            data = {'message': 'user added'}
            response = jsonify(data)
            response.status_code = 200
        except(InvalidCookie, InvalidUser,
               InvalidOrganization, sql.DataError,
               InvalidChannel, UserIsAlredyInChannel) as error:
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
            author_mail = msg.author_mail
            msgs_to_send.append({'timestamp': str(msg.timestamp),
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
            msgs_to_send.append({'timestamp': str(msg.timestamp),
                                 'author_mail': msg.author_mail,
                                 'body': msg.body})
        return msgs_to_send


class AdminLogin(Resource):
    """ manage login from admin webs """

    @classmethod
    def post(cls):
        """ login admins """
        content = request.get_json()
        mail = content['email']
        password = content['password']
        try:
            admin = Admin.check_if_admin(mail, password)
            token = admin.create_token()
            response = jsonify({'token': token})
            response.status_code = 200
        except NotAdminWeb as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


class AdminUsers(Resource):
    """ manage login from admin webs """

    @classmethod
    @jwt_required
    def options(cls):
        """post method"""

        response = jsonify({'message': 'options'})
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers["Access-Control-Allow-Methods"] = \
            'DELETE, POST, GET, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = \
            "Content-Type, Authorization, Accept"
        return response

    @classmethod
    @jwt_required
    def post(cls):
        """post method"""
        content = request.get_json()
        user_name = content['username']
        name = content['name']
        surname = content['surname']
        password = content['password']
        mail = content['mail']
        try:
            FbUser.add_user(mail, password, user_name, None)
            User.add_user(user_name, name, surname, mail, 0, 0, URL)
            response = jsonify({'message': 'user added'})
            response.status_code = 200
        except (SignedMail, InvalidMail) as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response

    @classmethod
    @jwt_required
    def get(cls):
        """ login admins """
        users = User.get_users()
        response = jsonify(users)
        response.status_code = 200
        return response

    @classmethod
    @jwt_required
    def delete(cls):
        """delete method"""
        mail = request.args['mail']
        try:
            FbUser.remove_user(mail)
            User.delete_user_with_mail(mail)
            response = jsonify({'message': 'user deleted'})
            response.status_code = 200
        except (InvalidMail) as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response

    @classmethod
    @jwt_required
    def put(cls):
        """delete method"""
        content = request.get_json()
        user_name = content['username']
        name = content['name']
        surname = content['surname']
        mail = content['mail']
        try:
            user = User.get_user_by_mail(mail)
            user.change(user_name, name, surname, user.url)
            FbUser.change_user(mail, user_name, user.url)
            response = jsonify({'message': 'User changed'})
            response.status_code = 200
        except (InvalidMail, SignedMail, UserNotRegistered) as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response


class AdminOrgas(Resource):
    """ manage login from admin webs """

    @classmethod
    @jwt_required
    def options(cls):
        """post method"""

        response = jsonify({'message': 'options'})
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers["Access-Control-Allow-Methods"] = \
            'DELETE, POST, GET, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = \
            "Content-Type, Authorization, Accept"
        return response

    @classmethod
    @jwt_required
    def post(cls):
        """post method"""
        content = request.get_json(force=True)
        mail = content['mail']
        org_name = content['name']
        description = content['description']
        welcome_message = content['welcomMsg']

        # pylint: disable=no-member
        try:
            creator_user = User.get_user_by_mail(mail)
            Organization.create(org_name, URL, creator_user,
                                description, welcome_message)
            data = {'message': 'orga added'}
            response = jsonify(data)
            response.status_code = 200
        except(InvalidOrganizationName, SignedOrganization) as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response

    @classmethod
    @jwt_required
    def get(cls):
        """ login admins """
        orgas = Organization.get_orgas()
        for orga in orgas:
            orga['creator'] = User.get_user_by_id(orga['creator']).mail
        response = jsonify(orgas)
        response.status_code = 200
        return response

    @classmethod
    @jwt_required
    def delete(cls):
        """ delete orga"""
        org_name = request.args['name']

        try:
            Organization.delete_organization(org_name)
            data = {'message': 'orga deleted'}

            response = jsonify(data)
            response.status_code = 200
        except InvalidOrganization as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response

    @classmethod
    @jwt_required
    def put(cls):
        """delete method"""
        content = request.get_json()
        org_name = content['name']
        description = content['description']
        welcome_message = content['welcomMsg']
        try:
            orga = Organization.get_organization_by_name(org_name)
            orga.change(description, welcome_message, orga.url)
            response = jsonify({'message': 'Orga changed'})
            response.status_code = 200
        except InvalidOrganization as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response


class InvalidWords(Resource):
    """manage invalid words """
    @classmethod
    def post(cls):
        """ adds invalid word to orga """
        content = request.get_json()
        word = content['word']
        org_name = content['org_name']
        try:
            orga = Organization.get_organization_by_name(org_name)
            orga.add_invalid_word(word)
            response = jsonify({'message': 'word added'})
            response.status_code = 200
        except NotAdminWeb as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    @classmethod
    def delete(cls):
        """ adds invalid word to orga """
        content = request.get_json()
        word = content['word']
        org_name = content['org_name']
        try:
            orga = Organization.get_organization_by_name(org_name)
            orga.delete_invalid_word(word)
            response = jsonify({'message': 'word deleted'})
            response.status_code = 200
        except NotAdminWeb as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    @classmethod
    def get(cls):
        """ adds invalid word to orga """
        try:
            orgas = Organization.get_orgas_with_words()
            response = jsonify(orgas)
            response.status_code = 200
        except NotAdminWeb as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


class AdminBots(Resource):
    """admin bot"""
    @classmethod
    @jwt_required
    def post(cls):
        """ adds new bot"""
        content = request.get_json()
        name = content['name']
        url = content['url']
        description = content['description']
        org_name = content['org_name']
        try:
            orga = Organization.get_organization_by_name(org_name)
            orga.add_bot(name, url, description)
            response = jsonify({'message': 'bot added'})
            response.status_code = 200
        except NotAdminWeb as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    @classmethod
    @jwt_required
    def get(cls):
        """get all bots"""
        retrieved_bots = Bot.get_all_bots()
        bots_to_send = []
        for bot in retrieved_bots:
            bots_to_send.append({'name': bot.name,
                                 'url': bot.url,
                                 'description': bot.description,
                                 'org_id': bot.organization_id})
        return bots_to_send


class ChannelInfoForBot(Resource):
    """ channel info for bots """
    @classmethod
    def get(cls, organization_name, channel_name):
        """ get info from channel """
        try:
            organization_id = Organization.\
                                get_organization_by_name(organization_name).id
            channel = Channel.get_channel_with_name(channel_name,
                                                    organization_id)
            return channel.get_channel_info()
        except InvalidChannel as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code

        return response


class UsersInfoForBot(Resource):
    """ user info for bots """
    @classmethod
    def get(cls, user_mail):
        """ get info from user """
        try:
            user = User.get_user_by_mail(user_mail)
            return user.get_user_info()
        except InvalidUser as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code

        return response


def save_msg(msg, user_id):
    """ save received msg to db """
    content = json.loads(msg)

    organization = content['organization']
    channel = content['channel']
    dm_dest = content['dm_dest']
    author_mail = User.get_user_by_id(user_id).mail
    body = content['body']
    body = replace_banned_words(body, organization)
    msg = Message.add_message(organization,
                              channel, dm_dest, author_mail, body)

    deliver_msg(body, organization, channel, author_mail, msg.timestamp,
                dm_dest)


def replace_banned_words(msg, organization):
    my_str = msg
    banned_words = Word.get_words_for_orga(organization)
    for word in banned_words:
        my_str = str.replace(my_str, word)

    return my_str
# pylint: disable=R0913
def deliver_msg(msg_body, org_name, channel_name, author_mail, timestamp,
                dm_dest):
    """ deliver msg to connected users. """

    org_id = Organization.get_organization_by_name(org_name).id

    msg_dict = {'msg_body': msg_body,
                'organization': org_name,
                'channel': channel_name,
                'dm_dest': dm_dest,
                'author_mail': author_mail,
                'timestamp': str(timestamp)}

    process_mentions(msg_body, org_name, channel_name, author_mail)

    if channel_name:
        users = Channel.get_users_in_channel(channel_name, org_id)
        for user in users:
            notify_user(user.mail.replace("@", "~at~"),
                        org_name + " - " + channel_name,
                        msg_body)
            if User.is_online(user.mail):
                sid = User.get_user_by_id(user.id).sid
                emit('message', msg_dict, room=sid)
    else:
        notify_user(dm_dest.replace("@", "~at~"),
                    "Message from " + author_mail,
                    msg_body)
        if User.is_online(dm_dest):
            sid = User.get_user_by_mail(dm_dest).sid
            emit('message', msg_dict, room=sid)


# pylint: enable=too-many-arguments
def notify_user(topic, title, body):
    """send notification to user with given info"""
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        topic=topic)
    messaging.send(message)


def process_mentions(msg_body, orga_name, channel_name, user_mail):
    """
    detect '@' char and derive behaviour
    according to usermention or bot invocation.
    """
    for word in msg_body.split():
        if word.startswith("@"):
            if is_user_mention(word):
                process_user_mention(word, orga_name, channel_name)
            else:
                process_bot_mention(word, msg_body.split(word, 1)[1][1:],
                                    orga_name, channel_name, user_mail)


def is_user_mention(word):
    """ check if the mention is mentioning a user email address """
    return "@" in word[1:]


def process_bot_mention(bot_name, arg, organization_name,
                        channel_name, user_mail):
    """ process bot """
    org_id = Organization.get_organization_by_name(organization_name).id

    bot = Bot.get_bot(bot_name)
    if bot is None:
        bot = Bot.get_bot(bot_name, org_id)
    if bot is None:
        return 

    response_text = requests.post(bot.url,
                                  data={'arg': arg,
                                        'user_mail': user_mail,
                                        'organization_name': organization_name,
                                        'channel_name': channel_name}).text

    if not response_text:
        return

    dm_dest = ""

    msg = Message.add_message(organization_name,
                              channel_name, dm_dest, bot_name, response_text)

    deliver_msg(response_text, organization_name, channel_name, bot_name,
                msg.timestamp, dm_dest)


def process_user_mention(word, orga_name, channel_name):
    """ define what happens when users get mentioned """
    topic = word[1:]
    title = "New mention in chat!"
    body = "You've been mentioned in " + orga_name + ", " + channel_name
    notify_user(topic, title, body)


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
    user.udpate_sid("")
