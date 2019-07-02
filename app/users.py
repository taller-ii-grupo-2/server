"""Module defining users model needed to define the db table."""
import re
from sqlalchemy.orm import validates
from app.fb_user import FbUser
from app import db, app
from app.organizations import Organization
from app.exceptions import InvalidMail, SignedMail
from app.exceptions import InvalidUser, UserIsNotAdmin
from app.exceptions import UserIsNotCreator, UserIsCreator
from app.associations import ORGS


# pylint: disable = R0902
# pylint: disable = too-many-public-methods
class User(db.Model):
    """ name table structure """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(), unique=True, nullable=False)
    name = db.Column(db.String(), nullable=False, server_default=' ')
    surname = db.Column(db.String(), nullable=False, server_default=' ')
    user_name = db.Column(db.String(), nullable=False, server_default=' ')
    longitude = db.Column(db.Float(), nullable=False)
    latitude = db.Column(db.Float(), nullable=False)
    url = db.Column(db.String(), nullable=False, server_default=' ')
    sid = db.Column(db.String(32), nullable=True, server_default=' ')
    organizations = db.relationship(
        'Organization',
        secondary=ORGS,
        backref=db.backref('users', lazy='subquery')
        )

    # pylint: disable = R0913
    def __init__(self, user_name, name, surname, mail,
                 longitude, latitude, url):
        """ initializes table """
        self.mail = mail
        self.user_name = user_name
        self.surname = surname
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.url = url

    def __repr__(self):
        """ assigns id"""
        return '<id {}>'.format(self.id)

    def serialize(self):
        """ table to json """
        organizations = []
        for orga in self.organizations:
            organizations.append(orga.get_name_and_channels())

        return {
            'name': self.name,
            'username': self.user_name,
            'surname': self.surname,
            'url': self.url,
            'organizations': organizations
        }

    # pylint: disable = R0913
    @staticmethod
    def add_user(user_name, name, surname, mail, longitude, latitude, url):
        """ adds user to table """
        user = User(
            mail=mail.lower(),
            user_name=user_name,
            surname=surname,
            name=name,
            longitude=longitude,
            latitude=latitude,
            url=url
        )
        db.session.add(user)  # pylint: disable = E1101
        db.session.commit()  # pylint: disable = E1101
        return user

    @staticmethod
    def login_user(token):
        """ adds user to table """
        cookie, expiration = FbUser.login_user(token)
        return cookie, expiration

    @staticmethod
    def get_user_claims(cookie):
        """ adds user to table """
        return FbUser.get_claims(cookie)

    @staticmethod
    def get_user_with_cookie(cookie):
        """ verifies if cookie is valid and return user id """
        fb_user = FbUser.get_user_with_cookie(cookie)
        return User.get_user_by_mail(fb_user.email)

    @validates('mail')
    # pylint: disable = unused-argument
    # pylint: disable = no-self-use
    def validate_email(self, key, mail):
        """validates mail format"""
        match = re.fullmatch(r"[^@]+@[^@]+\.[^@]+", mail)
        if not match:
            raise InvalidMail

        # pylint: disable = E1101
        user = db.session.query(User).filter_by(mail=mail).first()
        if user:
            raise SignedMail

        FbUser.get_user_by_email(mail)

        return mail

    @staticmethod
    def delete_all():
        """ delete entries in table """
        deletion = User.__table__.delete()
        db.session.execute(deletion)  # pylint: disable = E1101
        db.session.commit()  # pylint: disable = E1101

    @staticmethod
    def delete_user_with_mail(mail):
        """ delete entries in table """
        user = User.get_user_by_mail(mail)
        for orga in user.organizations:
            if orga.creator_user_id == user.id:
                Organization.delete_organization(orga.name)
        user.organizations.clear()
        user.channels.clear()
        User.query.filter_by(mail=mail).delete()
        db.session.commit()  # pylint: disable = E1101

    @staticmethod
    def get_user_by_mail(mail):
        """ search user by mail in db """
        # pylint: disable = E1101
        user = db.session.query(User).filter_by(mail=mail).first()
        if not user:
            raise InvalidUser
        return user

    @staticmethod
    def get_user_by_sid(sid):
        """ search user by sid in db """
        # pylint: disable = E1101
        return db.session.query(User).filter_by(sid=sid).first()

    @staticmethod
    def is_online(user_mail):
        """ say if user is connected via socket """
        # pylint: disable = E1101
        app.logger.info("is user online? " + str(user_mail))
        return bool(db.session.query(User).
                    filter_by(mail=user_mail).first().sid)

    def udpate_sid(self, sid):
        """ Update user's sid in table """
        # pylint: disable = E1101
        self.sid = sid
        db.session.commit()

    @staticmethod
    def get_user_by_id(user_id):
        """ search user by mail in db """
        # pylint: disable = E1101
        user = User.query.get(user_id)
        if not user:
            raise InvalidUser
        return user

    def get_organizations(self):
        """ return users organizations """
        orgas = []
        for orga in self.organizations:
            orgas.append(orga.serialize())
        # pylint: disable=no-member
        app.logger.info('orgas on get: ' + str(orgas))
        # pylint: enable=no-member
        return orgas

    def make_admin_user(self, user, orga):
        """ create a organization """
        if self.id != orga.creator_user_id:
            raise UserIsNotCreator
        orga.add_admin(user)

    def get_name_and_location(self):
        """get name and location of user"""
        return {
            'username': self.user_name,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

    def change(self, username, name, surname, url):
        """ changes user information """
        self.user_name = username
        self.surname = surname
        self.name = name
        self.url = url
        db.session.commit()  # pylint: disable = E1101
        FbUser.change_user(self.mail, username, url)

    @staticmethod
    def amount():
        """ get total amount of users """
        # pylint: disable = E1101
        return db.session.query(User).count()

    def remove_user_from_orga(self, orga, user):
        """ remove user form organization """

        if user.id == orga.creator_user_id:
            raise UserIsCreator

        if self not in orga.admins:
            raise UserIsNotAdmin

        orga.remove_user(user)

    def delete_orga(self, orga_name):
        """ remove organization """
        for orga in self.organizations:
            if orga.name == orga_name and self.id == orga.creator_user_id:
                self.organizations.remove(orga)
                db.session.commit()  # pylint: disable = E1101
                Organization.delete_organization(orga_name)
                return

        raise UserIsNotCreator

    def get_user_info(self):
        """" get users info as a md string """
        info = "# " + self.mail + "'s info:\n"
        info += "- Name: " + self.name + "\n"
        info += "- Surname: " + self.surname + "\n"
        info += "- Location:\n"
        info += "  - Lat.: " + str(self.latitude) + "\n"
        info += "  - Lon.: " + str(self.longitude) + "\n"
        info += "- Organizations:\n"
        for orga in self.organizations:
            info += "  -" + orga.name + "\n"

        return info

    @staticmethod
    def get_info_from(user_mail):
        """ get info from specified user """
        app.logger.info('getting users info...')  # pylint: disable = E1101
        try:
            user = User.get_user_by_mail(user_mail)
            return user.get_user_info()
        except InvalidUser:
            return ""

    @staticmethod
    def get_users():
        """ table to json """
        users = User.query.all()
        users_serialized = []

        for user in users:
            u_s = {
                'mail': user.mail,
                'name': user.name,
                'username': user.user_name,
                'surname': user.surname
            }
            users_serialized.append(u_s)

        return users_serialized
