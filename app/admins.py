""" admin model """
import json
from flask_jwt_extended import create_access_token
from app.exceptions import NotAdminWeb


FILE_URL = "./admins.json"


# pylint: disable = R0903
class Admin():
    """docstring for Admin"""

    def __init__(self, name, password):
        self.name = name
        self.password = password

    @staticmethod
    def check_if_admin(name, password):
        """ checks if user is admin web"""
        with open(FILE_URL) as file:
            data = json.load(file)

        for user in data['users']:
            if user['name'] == name and user['password'] == password:
                admin = Admin(name, password)
                return admin

        raise NotAdminWeb

    def create_token(self):
        """ create jwt token"""
        return create_access_token(identity=(self.name, self.password))
