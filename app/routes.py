"""File containing all endpoints in the app."""
import datetime
from flask import request, jsonify
from flask_restful import Resource
from app.users import User  # pylint: disable = syntax-error
from app.exceptions import InvalidMail, SignedMail, InvalidToken


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


class Register(Resource):
    """add users endpoint"""
    @classmethod
    def post(cls):
        """post method"""
        content = request.get_json()
        name = content['name']
        mail = content['mail']
        try:
            User.add_user(name, mail)
            response = jsonify("User added")
            response.status_code = 200
        except (InvalidMail, SignedMail) as error:
            response = jsonify(error.message)
            response.status_code = error.code
        return response


class Login(Resource):
    """login users endpoint"""
    @classmethod
    def post(cls):
        """put method"""
        content = request.get_json()
        token = content['token']
        expiration = datetime.timedelta(days=5)
        try:
            cookie = User.login_user(token, expiration)
            expires = datetime.datetime.now() + expiration
            response = jsonify("User added")
            response.set_cookie(
                'session', cookie, expires=expires, httponly=True, secure=True)
            response.status_code = 200
        except InvalidToken as error:
            response = jsonify(error.message)
            response.status_code = error.code
        return response


class DeleteUsers(Resource):
    """delete users endpoint"""
    @classmethod
    def delete(cls):
        """delete method"""
        User.delete_all()
