""" Module defininf de firebase auth """
import datetime
from firebase_admin import auth
from app.exceptions import InvalidCookie, InvalidToken
from app.exceptions import UserNotRegistered


class FbUser():
    """firebase user"""
    @staticmethod
    def get_user_by_email(mail):
        """obtain user with mail"""
        try:
            return auth.get_user_by_email(mail)
        except auth.AuthError:
            raise UserNotRegistered

    @staticmethod
    def change_user(mail, username, url):
        """obtain user with mail"""
        try:
            user = auth.get_user_by_email(mail)
            auth.update_user(
                user.uid,
                display_name=username,
                photo_url=url)
        except auth.AuthError:
            raise UserNotRegistered

    @staticmethod
    def login_user(token):
        """login user with token"""
        expiration = datetime.timedelta(days=5)
        try:
            expires = datetime.datetime.now() + expiration
            cookie = auth.create_session_cookie(token, expires_in=expiration)
            return cookie, expires
        except auth.AuthError:
            raise InvalidToken

    @staticmethod
    def get_claims(cookie):
        """logout user with coookie"""
        try:
            return auth.verify_session_cookie(cookie)
        except ValueError:
            raise InvalidCookie

    @staticmethod
    def get_user_with_cookie(cookie):
        """logout user with coookie"""
        # pylint: disable=no-member
        claims = FbUser.get_claims(cookie)
        # pylint: enable=no-member
        return auth.get_user(claims['uid'])

    @staticmethod
    def delete_user_with_email(mail):
        """delete user with mail"""
        user = auth.get_user_by_email(mail)
        auth.delete_user(user.uid)
