"""Module defining orgas model needed to define the db table.
This table is intended to be unique.
Another model will be defined for the tables used per organization.
"""
from datetime import datetime
import sqlalchemy.exc as sql
from sqlalchemy.orm import validates
from app import db
from app.exceptions import InvalidOrganizationName, AlreadyCreatedChannel
from app.exceptions import SignedOrganization, InvalidOrganization
from app.exceptions import UserIsAlredyInOrganization, UserNotInOrganization
from app.exceptions import InvalidChannel, UserIsAlreadyAdmin, UserIsNotAdmin
from app.exceptions import UserIsAlreadyInvited, UserIsNotInvited
from app.associations import ADMINS, INVS
from app.channels import Channel
from app.words import Word
from app import constant


# pylint: disable = R0904
class Organization(db.Model):
    """ name table structure """
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(constant.MAX_ORGANIZATION_NAME_LENGTH),
        nullable=False)
    url = db.Column(db.String(300))
    # In general, you will want to work with UTC dates and times in a server
    # application. This ensures that you are using uniform timestamps
    # regardless of where the users are located.
    # from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial
    # -part-iv-database
    creation_timestamp = db.Column(db.DateTime, index=True,
                                   default=datetime.utcnow)
    creator_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    channels = db.relationship('Channel', backref='organization', lazy=True)
    words = db.relationship('Word', backref='organization', lazy=True)
    invitations = db.relationship(
        'User',
        secondary=INVS,
        backref=db.backref('invites', lazy='subquery'))
    admins = db.relationship(
        'User',
        secondary=ADMINS,
        backref=db.backref('org_admin', lazy='subquery')
        )
    description = db.Column(
        db.String(constant.MAX_ORGANIZATION_DESCRIPTION_LENGTH),
        nullable=False)
    welcome_message = db.Column(
        db.String(constant.MAX_ORGANIZATION_WELCOME_MSG_LENGTH),
        nullable=False)

    # pylint: disable = R0913
    # pylint: disable = R0801
    def __init__(self, name, url, creator_user_id, description,
                 welcome_message):
        """ initializes table """
        self.name = name
        self.url = url
        self.creator_user_id = creator_user_id
        self.description = description
        self.welcome_message = welcome_message

    # pylint: disable = R0801
    def __repr__(self):
        """ assigns id"""
        return '<id: {}, org name: {}>'.format(self.id, self.name)

    def serialize(self):
        """ table to json """
        channels = []
        users = []
        for channel in self.channels:
            channels.append(channel.name)
        for user in self.users:
            users.append(user.name)
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'users': users,
            'channels': channels
        }

    # pylint: disable = R0913
    @staticmethod
    def add_orga(name, url, user_id, description, welcome_message):
        """ adds orga to table """
        try:
            orga = Organization(
                name=name,
                url=url,
                creator_user_id=user_id,
                description=description,
                welcome_message=welcome_message,
            )
            db.session.add(orga)  # pylint: disable = E1101
            db.session.commit()  # pylint: disable = E1101
        except (sql.DataError) as error:
            raise error
        return orga

    @staticmethod
    def create(name, url, user, description, welcome_message):
        """ creates orga with 2 channels and admin """
        orga = Organization.add_orga(name, url, user.id, description,
                                     welcome_message)
        orga.add_user_admin(user)
        orga.create_channel('General', False, user,
                            'General channel', 'Welcome')
        orga.create_channel('Random', False, user,
                            'Random channel', 'Welcome')
        return orga

    @validates('name')
    # pylint: disable = unused-argument
    # pylint: disable = no-self-use
    def validate_name(self, key, org_name):
        """validates mail format"""
        if len(org_name) > constant.MAX_ORGANIZATION_NAME_LENGTH:
            raise InvalidOrganizationName

        # pylint: disable = E1101
        orga = db.session.query(Organization). \
            filter_by(name=org_name).first()

        if orga:
            raise SignedOrganization
        return org_name

    @staticmethod
    def delete_all():
        """ delete entries in table """
        deletion = Organization.__table__.delete()
        db.session.execute(deletion)  # pylint: disable = E1101
        db.session.commit()  # pylint: disable = E1101

    def create_channel(self, name, private, user,
                       description, welcome_message):
        """ creates channel in organization """
        try:
            Channel.get_channel_with_name(name, self.id)
        except InvalidChannel:
            if user not in self.users:
                raise UserNotInOrganization
            channel = Channel.add_channel(name, private, user.id, description,
                                          welcome_message, self.id)
            channel.add_user(user)
            if not private:
                channel.add_users(self.users)
            return channel
        else:
            raise AlreadyCreatedChannel

    def get_channels_with_user(self, user_id):
        """ gets channels that have the user """
        channels = []
        for channel in self.channels:
            for user in channel.users:
                if user.id == user_id:
                    channels.append(channel.name)

        return channels

    @staticmethod
    def get_organization_by_name(name):
        """ get organization with name """
        # pylint: disable = E1101
        orga = db.session.query(Organization).filter_by(name=name).first()
        if not orga:
            raise InvalidOrganization
        return orga

    def add_user(self, new_user):
        """ adds user to organization """
        if new_user in self.users:
            raise UserIsAlredyInOrganization

        if new_user.id != self.creator_user_id:
            if new_user not in self.invitations:
                raise UserIsNotInvited

            self.invitations.remove(new_user)

        self.users.append(new_user)
        db.session.commit()  # pylint: disable = E1101
        for channel in self.channels:
            if not channel.private:
                channel.add_user(new_user)

    def add_user_to_channel(self, user, channel_name):
        """ adds user to the channel """
        channel = Channel.get_channel_with_name(channel_name, self.id)
        channel.add_user(user)

    def add_admin(self, user):
        """ makes the user and admin of the organization """
        if user not in self.users:
            raise UserNotInOrganization
        if user in self.admins:
            raise UserIsAlreadyAdmin
        self.admins.append(user)
        db.session.commit()  # pylint: disable = E1101

    def add_user_admin(self, user):
        """ adds user with admin acces """
        self.add_user(user)
        self.add_admin(user)

    def get_name_and_url(self):
        """ gets name and url of organization"""
        my_dict = {
            'name': self.name,
            'url': self.url
        }
        return my_dict

    def get_users_location(self):
        """ gets location of users in organization """
        users_location = []
        for user in self.users:
            users_location.append(user.get_name_and_location())
        return users_location

    def get_name_and_channels(self):
        """ gets name and channels of organization """
        channels = []
        for channel in self.channels:
            channels.append(channel.name)
        return {
            'name': self.name,
            'channels': channels
        }

    @staticmethod
    def delete_organization(org_name):
        """ delete organization from db """
        orga = Organization.get_organization_by_name(org_name)
        orga.delete_all_channels()
        orga.delete_all_invalid_words()
        orga.admins.clear()
        orga.users.clear()
        Organization.query.filter_by(name=orga.name).delete()
        db.session.commit()  # pylint: disable = E1101

    def delete_all_channels(self):
        """ delete all channels """
        for channel in self.channels:
            self.delete_channel(channel)

    def delete_channel(self, channel):
        """ delete channel in orga"""
        Channel.delete_channel(channel.name, self.id)

    def remove_invitation(self, user):
        """ remove user invitated to orga """
        self.invitations.remove(user)
        db.session.commit()  # pylint: disable = E1101

    def remove_admin(self, admin):
        """ removes admins from orga """
        self.admins.remove(admin)
        db.session.commit()  # pylint: disable = E1101

    def remove_user(self, user):
        """ removes user from orga """
        for channel in self.channels:
            if user in channel.users:
                channel.remove_user(user)

        self.users.remove(user)
        db.session.commit()  # pylint: disable = E1101

    def get_role_of_user(self, user):
        """ get role of user in organization """
        if user.id == self.creator_user_id:
            return "Creator"

        if user in self.admins:
            return "Admin"

        return "Member"

    def get_users_roles(self):
        """ get all users with roles """
        users = []
        for user in self.users:
            users.append({
                'mail': user.mail,
                'type': self.get_role_of_user(user)
                })
        return users

    def update_user(self, user_updating, user_to_update, role):
        """ update role of the user """
        if role == 'Admin' and user_updating.id == self.creator_user_id:
            self.add_admin(user_to_update)
        elif role == "Member" and user_updating in self.admins:
            self.remove_admin(user_to_update)
        else:
            raise UserIsNotAdmin

    def invite_user(self, user_to_add, user_inviting):
        """ invite user to orga """
        if user_inviting not in self.admins:
            raise UserIsNotAdmin
        if user_to_add in self.invitations:
            raise UserIsAlreadyInvited
        if user_to_add in self.users:
            raise UserIsAlredyInOrganization

        self.invitations.append(user_to_add)
        db.session.commit()  # pylint: disable = E1101

    def add_invalid_word(self, word):
        """ add invalid word to orga """
        word_to_add = Word.add_word(word, self.id)
        self.words.append(word_to_add)
        db.session.commit()  # pylint: disable = E1101

    def delete_invalid_word(self, word):
        """ deletes invalid word in orga """
        Word.delete_word(word, self.id)

    def delete_all_invalid_words(self):
        """ delete all words in orga """
        for word in self.words:
            self.delete_invalid_word(word.word)

    @staticmethod
    def get_orgas():
        """ get all organizations """
        orgas = Organization.query.all()
        orgas_serialized = []

        for orga in orgas:
            u_s = {
                'name': orga.name,
                'description': orga.description,
                'welcome': orga.welcome_message,
                'creator': orga.creator_user_id
            }
            orgas_serialized.append(u_s)

        return orgas_serialized

    def change(self, desc, welcome, url):
        """ change orga """
        self.description = desc
        self.welcome_message = welcome
        self.url = url
        db.session.commit()  # pylint: disable = E1101

    def get_words(self):
        """ get words of orga """
        string_words = []
        for word in self.words:
            string_words.append(word.word + ' ')

        return string_words

    @staticmethod
    def get_orgas_with_words():
        """ getall orgas with its words """
        orgas = Organization.query.all()
        org_and_words = []

        for orga in orgas:
            o_w = {
                'orga': orga.name,
                'words': orga.get_words()
            }
            org_and_words.append(o_w)

        return org_and_words

    @staticmethod
    def get_info_from(organization_name, channel_name):
        """ get infor from given org/channel """
        try:
            organization_id = Organization.\
                                get_organization_by_name(organization_name).id
            channel = Channel.get_channel_with_name(channel_name,
                                                    organization_id)
            return channel.get_channel_info()
        except InvalidChannel:
            return ""

    def get_amount_of_users(self):
        """retrieve amount of users"""
        return len(self.users)

    @staticmethod
    def get_orgas_with_amount_of_users():
        """ retrieve all orgas with amount of users"""

        orgas = Organization.query.all()
        org_and_users = []

        for orga in orgas:
            o_s = {
                'orga': orga.name,
                'users': orga.get_amount_of_users()
            }
            org_and_users.append(o_s)

        return org_and_users
