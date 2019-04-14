"""File containing all endpoints in the app."""
from flask import request, jsonify
from flask_restful import Resource
from app.models import User  # pylint: disable = syntax-error


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
        name = request.args.get('name')
        last_name = request.args.get('last_name')
        age = request.args.get('age')
        mail = request.args.get('mail')
        pais = request.args.get('pais')
        token = request.args.get('token')
        height = request.args.get('height')
        return User.add_user(name, last_name, age, mail, pais, token, height)
