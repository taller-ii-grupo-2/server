"""Module defining users model needed to define the db table."""
import re
from sqlalchemy.orm import validates
from firebase_admin import auth
from app import db
from app.exceptions import InvalidMail, SignedMail
from app.exceptions import InvalidToken, UserNotRegistered


class User(db.Model):
    """ name table structure """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(), unique=True, nullable=False)
    name = db.Column(db.String(), nullable=False, server_default=' ')

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
        try:
            user = User(
                mail=mail.lower(),
                name=name
            )
            db.session.add(user)  # pylint: disable = E1101
            db.session.commit()  # pylint: disable = E1101
        except (InvalidMail, SignedMail, UserNotRegistered) as error:
            raise error

    @staticmethod
    def login_user(token, expiration):
        """ adds user to table """
        try:
            cookie = auth.create_session_cookie(token,
                                                expires_in=expiration
                                                )
            return cookie
        except auth.AuthError:
            raise InvalidToken

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

        try:
            user = auth.get_user_by_email(mail)
        except:
            raise UserNotRegistered

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
        user = auth.get_user_by_email(mail)
        auth.delete_user(user.uid)

    @staticmethod
    def get_user_by_mail(mail):
        """ search user by mail in db """
        # pylint: disable = E1101
        return db.session.query(User).filter_by(mail=mail).first()
