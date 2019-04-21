from app.users import User
from app.exceptions import InvalidMail, SignedMail
import pytest


def test_addusers_incorrect_mail():
	
	with pytest.raises(InvalidMail):
		token = User.add_user('agustin','agustin.payasliangmail.com','asdasd')
	User.delete_all()
	

def test_addusers_correct_mail():

	token = User.add_user('agustin','agustin.payaslian@gmail.com','asdasd')
	user = User.get_user_by_mail('agustin.payaslian@gmail.com')
	assert 'agustin' in user.name
	User.delete_all()


def test_addusers_with_same_mail():
	password = 'asdasd'
	token = User.add_user('agustin','agustin.payaslian@gmail.com',password)
	with pytest.raises(SignedMail):
		token = User.add_user('agustin','agustin.payaslian@gmail.com',password)
	User.delete_all()


