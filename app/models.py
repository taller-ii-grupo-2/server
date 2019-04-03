from app import db

class User(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'last_name': self.last_name,
        }

    def add_name(self, username, email):
        try:
            user=User(
                username=username,
                email=email
            )
            db.session.add(user)
            db.session.commit()
            return "User added. user id={}".format(user.id)
        except Exception as e:
            return(str(e))
