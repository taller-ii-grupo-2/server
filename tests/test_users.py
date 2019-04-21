from app.users import User
from app.exceptions import InvalidMail, SignedMail, InvalidToken
import pytest
import datetime


def test_addusers_incorrect_mail():
	
	with pytest.raises(InvalidMail):
		User.add_user('agustin','agustin.payasliangmail.com')
	User.delete_all()
	

def test_addusers_correct_mail():

	User.add_user('agustin','agustin.payaslian@gmail.com')
	user = User.get_user_by_mail('agustin.payaslian@gmail.com')
	assert 'agustin' in user.name
	User.delete_all()


def test_addusers_with_same_mail():
	User.add_user('agustin','agustin.payaslian@gmail.com')
	with pytest.raises(SignedMail):
		User.add_user('agustin','agustin.payaslian@gmail.com')
	User.delete_all()

def test_incorrect_login_user():

	with pytest.raises(InvalidToken):
		expiration = datetime.timedelta(days=5)
		User.login_user('asdads',expiration)
	User.delete_all()


