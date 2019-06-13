""" admin model """
import json
from app.exceptions import NotAdminWeb


FILE_URL = "./admins.json"


# pylint: disable = R0903
class Admin():
    """docstring for Admin"""

    @staticmethod
    def check_if_admin(name, password):
        """ checks if user is admin web"""
        with open(FILE_URL) as file:
            data = json.load(file)

        for user in data['users']:
            if user['name'] == name and user['password'] == password:
                return 1

        raise NotAdminWeb
