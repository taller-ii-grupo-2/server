"""Module defining users model needed to define the db table."""
import re
import sqlalchemy.exc as sql
from sqlalchemy.orm import validates
from passlib.hash import pbkdf2_sha256 as sha256
from app import db
from app.exceptions import InvalidMail, SignedMail


class User(db.Model):
    """ name table structure """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    mail = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    # pylint: disable = R0913
    def __init__(self, name, mail, password):
        """ initializes table """
        self.name = name
        self.mail = mail
        self.password = password

    def __repr__(self):
        """ assigns id"""
        return '<id {}>'.format(self.id)

    def serialize(self):
        """ table to json """
        return {
            'id': self.id,
            'name': self.name,
            'mail': self.mail,
            'password': self.password
        }

    # pylint: disable = R0913
    @staticmethod
    def add_user(name, mail, password):
        """ adds user to table """
        try:
            user = User(
                name=name,
                mail=mail,
                password=User.generate_hash(password)
            )
            db.session.add(user)  # pylint: disable = E1101
            db.session.commit()  # pylint: disable = E1101
        except (sql.DataError, InvalidMail, SignedMail) as error:
            raise error
        return user

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
    def generate_hash(password):
        """uses criptographic function to hide password on db"""
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hashed_password):
        """ verifies password """
        return sha256.verify(password, hashed_password)

    @staticmethod
    def delete_all():
        """ delete entries in table """
        deletion = User.__table__.delete()
        db.session.execute(deletion)  # pylint: disable = E1101
        db.session.commit()  # pylint: disable = E1101
