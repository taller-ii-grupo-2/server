import os
from app import app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.users import User
from app.organizations import Organization
from app.channels import Channel
from app.words import Word

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)





if __name__ == '__main__':
    manager.run()
