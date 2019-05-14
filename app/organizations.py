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
from app.exceptions import InvalidChannel, UserIsAlreadyAdmin
from app.associations import ADMINS
from app.channels import Channel
from app import constant


class Organization(db.Model):
    """ name table structure """
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(constant.MAX_ORGANIZATION_NAME_LENGTH),
        nullable=False)
    url = db.Column(db.String())
    # In general, you will want to work with UTC dates and times in a server
    # application. This ensures that you are using uniform timestamps
    # regardless of where the users are located.
    # from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial
    # -part-iv-database
    creation_timestamp = db.Column(db.DateTime, index=True,
                                   default=datetime.utcnow)
    creator_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    channels = db.relationship('Channel', backref='organization', lazy=True)
    admins = db.relationship(
        'User',
        secondary=ADMINS,
        backref=db.backref('org_admin', lazy='subquery')
        )

    # pylint: disable = R0913
    # pylint: disable = R0801
    def __init__(self, name, url, creator_user_id):
        """ initializes table """
        self.name = name
        self.url = url
        self.creator_user_id = creator_user_id

    # pylint: disable = R0801
    def __repr__(self):
        """ assigns id"""
        return '<id: {}, org name: {}>'.format(self.id, self.name)

    def serialize(self):
        """ table to json """
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'creation_timestamp': self.creation_timestamp,
            'creator_user_id': self.creator_user_id
        }

    # pylint: disable = R0913
    @staticmethod
    def add_orga(name, url, user_id):
        """ adds orga to table """
        try:
            orga = Organization(
                name=name,
                url=url,
                creator_user_id=user_id
            )
            db.session.add(orga)  # pylint: disable = E1101
            db.session.commit()  # pylint: disable = E1101
        except (sql.DataError) as error:
            raise error
        return orga

    @staticmethod
    def create(name, url, user):
        """ creates orga with 2 channels and admin """
        orga = Organization.add_orga(name, url, user.id)
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
                    channels.append(channel)

        return channels

    @staticmethod
    def get_organization_by_name(name):
        """ get organization with name """
        # pylint: disable = E1101
        orga = db.session.query(Organization).filter_by(name=name).first()
        if not orga:
            raise InvalidOrganization
        return orga

    def add_user(self, user):
        """ adds user to organization """
        if user in self.users:
            raise UserIsAlredyInOrganization
        self.users.append(user)
        db.session.commit()  # pylint: disable = E1101
        for channel in self.channels:
            if not channel.private:
                channel.add_user(user)

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
