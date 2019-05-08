"""Module dedicated to the app config."""
import os


# pylint: disable = too-few-public-methods
class Config():
    """Base class for config. Later classes can hereditate from this one."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Production class for config."""
    DEBUG = False


class StagingConfig(Config):
    """Staging class for config."""
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    """Development class for config."""
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """Testing class for config."""
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True
