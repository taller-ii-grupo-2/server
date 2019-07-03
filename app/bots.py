"""Bots model"""
import sqlalchemy.exc as sql
from app import db
from app import constant


class Bot(db.Model):
    """ name table structure """
    __tablename__ = 'bots'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(constant.MAX_BOT_NAME_LENGTH), nullable=False,
                     unique=True)
    url = db.Column(db.String(constant.MAX_BOT_URL_LENGTH), nullable=False)
    description = db.Column(db.String(constant.MAX_BOT_DESCRIPTION_LENGTH),
                            nullable=False)
    organization_name = db.Column(db.String(constant.
                                            MAX_ORGANIZATION_NAME_LENGTH),
                                  nullable=True)

    # pylint: disable = R0913

    def __init__(self, name, url, description, organization_name):
        """ initializes table """
        self.name = name
        self.url = url
        self.description = description
        self.organization_name = organization_name

    # pylint: disable = R0801
    def __repr__(self):
        """ assigns id"""
        return '<id: {}, name: {}, url: {}, desc: {}, org id: {}>'.\
               format(self.id, self.name, self.url, self.description,
                      self.organization_name)

    # pylint: disable = R0801
    def serialize(self):
        """ table to json """

        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'description': self.description,
            'organization_name': self.organization_name,
        }

    @staticmethod
    def add_bot(name, url, description, organization_name):
        """ adds bot to table """
        try:
            bot = Bot(
                name=name,
                url=url,
                description=description,
                organization_name=organization_name
            )
            db.session.add(bot)  # pylint: disable = E1101
            db.session.commit()  # pylint: disable = E1101
        except (sql.DataError) as error:
            raise error
        return bot

    @staticmethod
    def get_all_bots():
        """ gets all bots """
        return Bot.query.all()

    @staticmethod
    def get_bot(name, org_name=""):
        """ gets bot in org by name """
        return Bot.query.filter_by(name=name,
                                   organization_name=org_name).first()

    def update_bot(self, url, description, org_name):
        """updates bot info"""
        self.url = url
        self.description = description
        self.organization_name = org_name

    @staticmethod
    def delete_bot(name):
        """ deletes bot """
        Bot.query.filter_by(name=name).delete()
        db.session.commit()  # pylint: disable = E1101
