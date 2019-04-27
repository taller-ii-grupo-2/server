"""File containing all endpoints in the app."""
from flask import request, jsonify
from flask_restful import Resource
from app.users import User  # pylint: disable = syntax-error
from app.exceptions import InvalidMail, SignedMail
from app import app


class Index(Resource):
    """home endpoint"""
    @classmethod
    def get(cls):
        """get mmethod"""
        app.logger.info('home visited')  # pylint: disable=no-member


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
            user = User.add_user(name, mail, password)
            data = {'id': user.id,
                    'message': 'User added.'
                    }
            response = jsonify(data)
            response.status_code = 200
        except (InvalidMail, SignedMail) as error:
            response = jsonify(error.message)
            response.status_code = 400
        return response
