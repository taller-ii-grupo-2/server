"""Module defining all models needed to define the db tables."""
import sqlalchemy.exc as sql
from app import db


class User(db.Model):
    """ name table structure """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    last_name = db.Column(db.String())
    age = db.Column(db.Integer())
    mail = db.Column(db.String())
    pais = db.Column(db.String())
    token = db.Column(db.String())

    # pylint: disable = R0913
    def __init__(self, name, last_name, age, mail, pais, token):
        """ initializes table """
        self.name = name
        self.last_name = last_name
        self.age = age
        self.mail = mail
        self.pais = pais
        self.token = token

    def __repr__(self):
        """ assigns id"""
        return '<id {}>'.format(self.id)

    def serialize(self):
        """ table to json """
        return {
            'id': self.id,
            'name': self.name,
            'last_name': self.last_name,
            'age': self.age,
            'mail': self.mail,
            'pais': self.pais,
            'token': self.token
        }

    # pylint: disable = R0913
    @staticmethod
    def add_user(name, last_name, age, mail, pais, token):
        """ adds user to table """
        try:
            user = User(
                name=name,
                last_name=last_name,
                age=age,
                mail=mail,
                pais=pais,
                token=token
            )
            db.session.add(user)  # pylint: disable = E1101
            db.session.commit()  # pylint: disable = E1101
            return "User added. user id={}".format(user.id)
        except sql.DataError as error:
            return str(error)
