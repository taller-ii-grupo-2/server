import os
from app import app,db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
from app.models import Name


if __name__ == '__main__':
    manager.run()
