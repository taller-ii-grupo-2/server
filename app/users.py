"""Module defining users model needed to define the db table."""
import re
from sqlalchemy.orm import validates
from app.fb_user import FbUser
from app.organizations import Organization
from app import db
from app.exceptions import InvalidMail, SignedMail
from app.associations import ORGS


class User(db.Model):
    """ name table structure """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(), unique=True, nullable=False)
    name = db.Column(db.String(), nullable=False, server_default=' ')
    organizations = db.relationship(
        'Organization',
        secondary=ORGS,
        backref=db.backref('users', lazy='subquery')
        )

    # pylint: disable = R0913
    def __init__(self, name, mail):
        """ initializes table """
        self.mail = mail
        self.name = name

    def __repr__(self):
        """ assigns id"""
        return '<id {}>'.format(self.id)

    def serialize(self):
        """ table to json """
        return {
            'id': self.id,
            'mail': self.mail,
            'name': self.name
        }

    # pylint: disable = R0913
    @staticmethod
    def add_user(name, mail):
        """ adds user to table """
        user = User(
            mail=mail.lower(),
            name=name
        )
        db.session.add(user)  # pylint: disable = E1101
        db.session.commit()  # pylint: disable = E1101

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
        User.query.filter_by(mail=mail).delete()
        db.session.commit()  # pylint: disable = E1101
        # FbUser.delete_user_with_email(mail)

    @staticmethod
    def get_user_by_mail(mail):
        """ search user by mail in db """
        # pylint: disable = E1101
        return db.session.query(User).filter_by(mail=mail).first()

    def create_organization(self, org_name):
        """ create a organization """
        orga = Organization.add_orga(org_name, self.id)
        self.organizations.append(orga)
        db.session.commit()  # pylint: disable = E1101
        return orga.name

    def get_organizations(self):
        """ create a organization """
        orgas = []
        for orga in self.organizations:
            orgas.append(orga.name)
        return orgas
