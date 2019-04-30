"""Module defining orgas model needed to define the db table.
This table is intended to be unique.
Another model will be defined for the tables used per organization.
"""
from datetime import datetime
import sqlalchemy.exc as sql
from sqlalchemy.orm import validates
from app import db
from app.exceptions import InvalidOrganizationName
from app.exceptions import SignedOrganization
from app import constant


class Organization(db.Model):
    """ name table structure """
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(constant.MAX_ORGANIZATION_NAME_LENGTH),
                         nullable=False)

    # In general, you will want to work with UTC dates and times in a server
    # application. This ensures that you are using uniform timestamps
    # regardless of where the users are located.
    # from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial
    # -part-iv-database
    creation_timestamp = db.Column(db.DateTime, index=True,
                                   default=datetime.utcnow)
    creator_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # pylint: disable = R0913
    def __init__(self, org_name, creator_user_id):
        """ initializes table """
        self.org_name = org_name
        self.creator_user_id = creator_user_id

    def __repr__(self):
        """ assigns id"""
        return '<id: {}, org name: {}>'.format(self.id, self.org_name)

    def serialize(self):
        """ table to json """
        return {
            'id': self.id,
            'org_name': self.org_name,
            'creation_timestamp': self.creation_timestamp,
            'creator_user_id': self.creator_user_id
        }

    # pylint: disable = R0913
    @staticmethod
    def add_orga(org_name, creator_user_id):
        """ adds orga to table """
        try:
            orga = Organization(
                org_name=org_name,
                creator_user_id=creator_user_id
            )
            db.session.add(orga)  # pylint: disable = E1101
            db.session.commit()  # pylint: disable = E1101
        except (sql.DataError) as error:
            raise error
        return orga

    @validates('org_name')
    # pylint: disable = unused-argument
    # pylint: disable = no-self-use
    def validate_email(self, key, org_name):
        """validates mail format"""
        if len(org_name) > constant.MAX_ORGANIZATION_NAME_LENGTH:
            raise InvalidOrganizationName

        # pylint: disable = E1101
        orga = db.session.query(Organization). \
            filter_by(org_name=org_name).first()

        if orga:
            raise SignedOrganization
        return org_name

    @staticmethod
    def delete_all():
        """ delete entries in table """
        deletion = Organization.__table__.delete()
        db.session.execute(deletion)  # pylint: disable = E1101
        db.session.commit()  # pylint: disable = E1101
