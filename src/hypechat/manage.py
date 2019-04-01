"""
db manager
"""
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
# pylint: disable = no-name-in-module
from __init__ import app, db

# pylint: disable = invalid-name
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
