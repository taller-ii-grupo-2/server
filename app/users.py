"""Module defining users model needed to define the db table."""
import re
import sqlalchemy.exc as sql
from sqlalchemy.orm import validates
from firebase_admin import auth
from app import db
from app.exceptions import InvalidMail, SignedMail


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
    def add_user(name, mail, password):
        """ adds user to table """
        try:
            user = User(
                mail=mail,
                name=name
            )
            db.session.add(user)  # pylint: disable = E1101
            db.session.commit()  # pylint: disable = E1101
        except (sql.DataError, InvalidMail, SignedMail) as error:
            raise error

        user_id = str(user.id)
        auth.create_user(
            uid=user_id,
            email=mail,
            password=password,
            display_name=name
            )
        return auth.create_custom_token(user_id)

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
        return mail

    @staticmethod
    def delete_all():
        """ delete entries in table """
        deletion = User.__table__.delete()
        db.session.execute(deletion)  # pylint: disable = E1101
        db.session.commit()  # pylint: disable = E1101
        for user in auth.list_users().iterate_all():
            auth.delete_user(user.uid)

    @staticmethod
    def get_user_by_mail(mail):
        """ search user by mail in db """
        # pylint: disable = E1101
        return db.session.query(User).filter_by(mail=mail).first()
