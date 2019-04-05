"""Module dedicated to the app config."""
import os


# pylint: disable = too-few-public-methods
class Config():
    """Base class for config. Later classes can hereditate from this one."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
