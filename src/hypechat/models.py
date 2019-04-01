"""
Define models used in the server
"""
from sqlalchemy import exc
# pylint: disable = no-name-in-module
from __init__ import db


# pylint: disable = missing-docstring
class Name(db.Model):
    __tablename__ = 'names'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    last_name = db.Column(db.String())

    def __init__(self, name, last_name):
        self.name = name
        self.last_name = last_name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'last_name': self.last_name,
        }

    def add_name(self, name, last_name):
        try:
            name = Name(
                name=name,
                last_name=last_name
            )
            self.db.session.add(name)
            self.db.session.commit()
            return "Name added. name id={}".format(name.id)
        except exc.SQLAlchemyError as exception:
            return str(exception)
