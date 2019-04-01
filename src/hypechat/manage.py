import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from init import app,db

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
from models import Name


if __name__ == '__main__':
    manager.run()