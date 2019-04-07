"""Module defining all models needed to define the db tables."""
from app import db


class User(db.Model):
    """ name table structure """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    last_name = db.Column(db.String())
    age = db.Column(db.Integer())
    mail = db.Column(db.String())

    def __init__(self, name, last_name,age,mail):
        self.name = name
        self.last_name = last_name
        self.age = age
        self.mail = mail
        
    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'last_name': self.last_name,
            'age': self.age,
            'mail': self.mail
        }

    def add_user(name, last_name,age,mail):
        try:
            user=User(
                name=name,
                last_name=last_name,
                age=age,
                mail=mail
            )
            db.session.add(user)
            db.session.commit()
            return "User added. user id={}".format(user.id)
        except Exception as e:
            return(str(e))
