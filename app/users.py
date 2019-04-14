"""Module defining all models needed to define the db tables."""
import sqlalchemy.exc as sql
from app import db


class User(db.Model):
    """ name table structure """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    mail = db.Column(db.String())
    password = db.Column(db.String())

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
                password=password
            )
            db.session.add(user)  # pylint: disable = E1101
            db.session.commit()  # pylint: disable = E1101
            return "User added. user id={}".format(user.id)
        except sql.DataError as error:
            return str(error)
