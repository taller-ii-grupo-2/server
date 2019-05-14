"""Module defining model needed to define the db table of each organization's
table. Unlike the Organization model, this is to create one table per oorga.
"""
from datetime import datetime
import sqlalchemy.exc as sql
from sqlalchemy.orm import validates
from app import db
from app.exceptions import SignedOrganization
from app.exceptions import EventNameTooLong, InvalidEvent
from app import constant
from sqlalchemy.orm import relationship


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.String(constant.MAX_ORGANIZATION_NAME_LENGTH),
                         nullable=True)

    channel = db.Column(db.String(constant.MAX_CHANNEL_NAME_LENGTH),
                         nullable=True)
    
    # destinatario en caso de msj directo.
    dm_dest = db.Column(db.Integer, nullable=True)

    # In general, you will want to work with UTC dates and times in a server
    # application. This ensures that you are using uniform timestamps
    # regardless of where the users are located.
    # from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial
    # -part-iv-database
    timestamp = db.Column(db.DateTime, index=True,
                                   default=datetime.utcnow)
    author_id = db.Column(db.Integer)

    body = db.Column(db.String(constant.MAX_MSG_BODY_LENGTH), nullable=False)
#    events_author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#    user = relationship("User")

    # pylint: disable = R0913
    def __init__(self, event_type, events_author_id):
        """ initializes table """
        self.event_type = event_type
        self.events_author_id = events_author_id

    def __repr__(self):
        """ assigns id"""
        return '<id: {}, event type: {}, events author: {}, timestamps: {}>'.format(self.event_id, self.event_type, self.events_author_id, self.event_timestamp)

    def serialize(self):
        """ table to json """
        return {
            'event_id': self.event_id,
            'event_type': self.event_type,
            'event_timestamp': self.event_timestamp,
            'events_author_id': self.events_author_id
        }

    # pylint: disable = R0913
    @staticmethod
    def add_message(org, channel, dm_dest, author_id, body):
        """ adds msg to table """
        try:
            msg = Message(
                    organization = org,
                    channel = channel,
                    dm_dest = dm_dest,
                    author_id = author_id,
                    body = body
            )
            db.session.add(msg)  # pylint: disable = E1101
            db.session.commit()  # pylint: disable = E1101
        except (sql.DataError) as error:
            raise error
        app.logger.info('added msg to db: ' + msg)
        return msg


#    @staticmethod
#    def delete_all():
#        """ delete entries in table """
#        deletion = Organization.__table__.delete()
#        db.session.execute(deletion)  # pylint: disable = E1101
#        db.session.commit()  # pylint: disable = E1101
