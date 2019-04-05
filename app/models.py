"""Module defining all models needed to define the db tables."""
from app import db


class Name(db.Model):
    """Name table structure."""
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
        """not sure what this does"""
        return {
            'id': self.id,
            'name': self.name,
            'last_name': self.last_name,
        }

# pylint: disable = no-member
    @staticmethod
    def add_name(name, last_name):
        """add name to db"""
        try:
            name = Name(
                name=name,
                last_name=last_name
            )
            db.session.add(name)
            db.session.commit()
            return "Name added. name id={}".format(name.id)
        except Exception as exception:  # pylint: disable = broad-except
            return str(exception)
