from init import db

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

    def add_name(name, last_name):
        try:
            name=Name(
                name=name,
                last_name=last_name
            )
            db.session.add(name)
            db.session.commit()
            return "Name added. name id={}".format(name.id)
        except Exception as e:
            return("error in models.py, add_name" +  str(e))
