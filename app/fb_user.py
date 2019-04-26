"""Module defining fireabase auth."""
from firebase_admin import auth
from app.exceptions import InvalidToken


class FbUser():

	@staticmethod
	def get_user_by_email(mail):
		return auth.get_user_by_email(mail)

	@staticmethod
	def login_user(token, expiration):

		try:
			return auth.create_session_cookie(token, expires_in=expiration)
		except auth.AuthError:
			raise InvalidToken


	@staticmethod
	def delete_user_with_email(mail):
		user = auth.get_user_by_email(mail)
		auth.delete_user(user.uid)