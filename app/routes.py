"""File containing all endpoints in the app."""
import json
import flask
from flask import request, jsonify
from flask_restful import Resource
from app.users import User  # pylint: disable = syntax-error
from app.exceptions import InvalidOrganizationName
from app.exceptions import SignedOrganization
from app import app
from app.exceptions import InvalidMail, SignedMail
from app.exceptions import InvalidToken, UserNotRegistered
from app.exceptions import InvalidCookie


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
            response = jsonify({'message': 'User added'})
            response.status_code = 200
        except (InvalidMail, SignedMail, UserNotRegistered) as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response


class Login(Resource):
    """login users endpoint"""
    @classmethod
    def post(cls):
        """post method"""
        content = request.get_json()
        token = content['token']
        try:
            cookie, expires = User.login_user(token)
            response = jsonify({'message': 'User logged'})
            response.set_cookie(
                'session', cookie, expires=expires, httponly=True, secure=True)
            response.status_code = 200
        except InvalidToken as error:
            response = jsonify({'message': error.message})
            response.status_code = error.code
        return response


class Logout(Resource):
    """logout users endpoint"""
    @classmethod
    def post(cls):
        """post method"""
        session_cookie = request.cookies.get('session')
        try:
            User.get_user_claims(session_cookie)
            response = flask.make_response(flask.redirect('/login'))
            response.set_cookie('session', expires=0)
            response.data = json.dumps({'message': 'User Logged out'})
            response.status_code = 200
            return response
        except InvalidCookie as error:
            response = flask.make_response(flask.redirect('/login'))
            response.set_cookie('session', expires=0)
            response.data = json.dumps({'message': error.message})
            response.status_code = error.code
            return response


class DeleteUsers(Resource):
    """delete users endpoint"""
    @classmethod
    def delete(cls):
        """delete method"""
        User.delete_all()


class DeleteUser(Resource):
    """delete users endpoint"""
    @classmethod
    def delete(cls):
        """delete method"""
        content = request.get_json()
        mail = content['mail']
        User.delete_user_with_mail(mail)


class CreateOrganization(Resource):
    """create new orga"""
    @classmethod
    def post(cls):
        """post method"""
        content = request.get_json()
        org_name = content['org_name']
        session_cookie = request.cookies.get('session')
        try:
            user = User.get_user_with_cookie(session_cookie)
            orga_name = user.create_organization(org_name)
            data = {'name': orga_name,
                    'message': 'orga added'
                    }
            response = jsonify(data)
            response.status_code = 200
        except(InvalidOrganizationName, SignedOrganization) as error:
            response = jsonify(error.message)
            response.status_code = error.code
        except InvalidCookie:
            return flask.redirect('/login')
        return response


class ShowOrganization(Resource):
    """create new orga"""
    @classmethod
    def post(cls):
        """post method"""
        session_cookie = request.cookies.get('session')
        try:
            user = User.get_user_with_cookie(session_cookie)
            orgas = user.get_organizations()
            response = jsonify(orgas)
            response.status_code = 200
        except InvalidCookie:
            return flask.redirect('/login')
        return response
