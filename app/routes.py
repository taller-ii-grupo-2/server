"""File containing all endpoints in the app."""
from flask import request, jsonify
from flask_restful import Resource
from app.users import User  # pylint: disable = syntax-error
from app.exceptions import InvalidMail, SignedMail


class Index(Resource):
    """home endpoint"""
    @classmethod
    def get(cls):
        """get mmethod"""
        return "Hello, World!"


class Android(Resource):
    """android endpoint"""
    @classmethod
    def get(cls):
        """get mmethod"""
        return "Hello, android"


class AllUsers(Resource):
    """all users endpoint"""
    @classmethod
    def get(cls):
        """get mmethod"""
        try:
            users = User.query.all()
            return jsonify([e.serialize() for e in users])
        except Exception as exception:  # pylint: disable = broad-except
            return str(exception)


class AddUsers(Resource):
    """add users endpoint"""
    @classmethod
    def post(cls):
        """post method"""
        content = request.get_json()
        name = content['name']
        mail = content['mail']
        password = content['password']
        try:
            token = User.add_user(name, mail, password)
            response = jsonify(str(token))
            response.status_code = 200
        except (InvalidMail, SignedMail) as error:
            response = jsonify(error.message)
            response.status_code = 400
        return response

class DeleteUsers(Resource):
    """delete users endpoint"""
    @classmethod
    def delete(cls):
        """delete method"""
        User.delete_all()
