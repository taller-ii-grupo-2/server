"""Channel model"""
import sqlalchemy.exc as sql
from sqlalchemy.orm import validates
from app import db
from app import constant
from app.exceptions import InvalidChannelName, UserIsAlredyInChannel
from app.exceptions import InvalidChannel
from app.associations import USRS


class Channel(db.Model):
    """ name table structure """
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(constant.MAX_ORGANIZATION_NAME_LENGTH),
        nullable=False)
    private = db.Column(db.Boolean())
    creator_user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    description = db.Column(db.String())
    welcome_message = db.Column(db.String())
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'),
                                nullable=False)
    users = db.relationship('User', secondary=USRS)

    # pylint: disable = R0913
    def __init__(self, name, private, creator_user_id, description,
                 welcome_message, organization_id):
        """ initializes table """
        self.name = name
        self.private = private
        self.creator_user_id = creator_user_id
        self.description = description
        self.welcome_message = welcome_message
        self.organization_id = organization_id

    # pylint: disable = R0801
    def __repr__(self):
        """ assigns id"""
        return '<id: {}, org name: {}>'.format(self.id, self.name)

    # pylint: disable = R0801
    def serialize(self):
        """ table to json """

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'welcome_message': self.welcome_message
        }

    @staticmethod
    def add_channel(name, private, user_id, description,
                    welcome_message, organization_id):
        """ adds channel to table """
        try:
            channel = Channel(
                name=name,
                private=private,
                creator_user_id=user_id,
                description=description,
                welcome_message=welcome_message,
                organization_id=organization_id
            )
            db.session.add(channel)  # pylint: disable = E1101
            db.session.commit()  # pylint: disable = E1101
        except (sql.DataError) as error:
            raise error
        return channel

    @validates('name')
    # pylint: disable = unused-argument
    # pylint: disable = no-self-use
    def validate_name(self, key, name):
        """validates name format"""
        if len(name) > constant.MAX_ORGANIZATION_NAME_LENGTH:
            raise InvalidChannelName

        return name

    def add_user(self, user):
        """ adds user to channel """
        if user in self.users:
            raise UserIsAlredyInChannel
        self.users.append(user)
        db.session.commit()  # pylint: disable = E1101

    @staticmethod
    def get_channel_with_name(name, org_id):
        """ get channel with of organization with name """
        channel = Channel.query.filter_by(name=name,
                                          organization_id=org_id).first()
        if not channel:
            raise InvalidChannel
        return channel

    def add_users(self, users):
        """ add multiple users to channel """
        for user in users:
            try:
                self.add_user(user)
            except UserIsAlredyInChannel:
                continue

    @staticmethod
    def get_users_in_channel(name, org_id):
        """ get users in channel of orga """
        return Channel.get_channel_with_name(name, org_id).users
