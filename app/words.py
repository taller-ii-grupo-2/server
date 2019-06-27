"""Words model"""
import sqlalchemy.exc as sql
from app import db


class Word(db.Model):
    """ name table structure """
    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'),
                                nullable=False)

    # pylint: disable = R0913
    def __init__(self, word, organization_id):
        """ initializes table """
        self.word = word
        self.organization_id = organization_id

    # pylint: disable = R0801
    def __repr__(self):
        """ assigns id"""
        return '<id: {}, org name: {}>'.format(self.id, self.word)

    # pylint: disable = R0801
    def serialize(self):
        """ table to json """

        return {
            'id': self.id,
            'word': self.word
        }

    @staticmethod
    def add_word(word, organization_id):
        """ adds word to table """
        try:
            word = Word(
                word=word,
                organization_id=organization_id
            )
            db.session.add(word)  # pylint: disable = E1101
            db.session.commit()  # pylint: disable = E1101
        except (sql.DataError) as error:
            raise error
        return word

    @staticmethod
    def get_word(word, org_id):
        """ gets word """
        return Word.query.filter_by(word=word,
                                    organization_id=org_id).first()

    @staticmethod
    def delete_word(word, org_id):
        """ deletes word """
        Word.query.filter_by(word=word,
                             organization_id=org_id).delete()
        db.session.commit()  # pylint: disable = E1101

    def get_words_for_orga(organization_name):
        """ gets words for given orga"""
        org_id = Organization.get_organization_by_name(organization_name).id
        return Word.query.filter_by(organization_id=org_id).all()

