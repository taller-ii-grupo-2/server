"""config file"""
import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))


# pylint: disable=too-few-public-methods
class Config():
    """Base Config class"""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'


class ProductionConfig(Config):
    """Config for production env."""
    DEBUG = False


class StagingConfig(Config):
    """Config for staging env."""
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    """Config for dev env."""
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """Config for testing env."""
    TESTING = True
