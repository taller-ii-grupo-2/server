from app.users import User
from app.exceptions import InvalidMail, SignedMail, InvalidToken, UserNotRegistered
from firebase_admin import auth
import pytest
from pytest_mock import mocker
import os
from app import db
import datetime


def test_addusers_incorrect_mail():
    with pytest.raises(InvalidMail):
        User.add_user('agustin','agustin.payasliangmail.com')
	

def test_addusers_correct_mail(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	User.add_user('agustin','agustin.payaslian@gmail.com')
	user = User.get_user_by_mail('agustin.payaslian@gmail.com')
	assert 'agustin' in user.name
	User.delete_user_with_mail('agustin.payaslian@gmail.com')
	

def test_addusers_with_same_mail(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	User.add_user('agustin','agustin.payaslian@gmail.com')
	with pytest.raises(SignedMail):
		User.add_user('agustin','agustin.payaslian@gmail.com')
	User.delete_user_with_mail('agustin.payaslian@gmail.com')

def test_addusers_not_signed_in_firebase(mocker):
	mocker.patch('app.fb_user.FbUser.get_user_by_email',side_effect= UserNotRegistered )
	with pytest.raises(UserNotRegistered):
		User.add_user('agustin','agustin.payaslian@gmail.com')

def test_incorrect_login_user():

	with pytest.raises(InvalidToken):
		User.login_user('asdads')

def test_correct_login_user(mocker):
	mock_cookie = 'ksgdfhgs<hgfskjfgjksgfkjsgfjsgfjksdgfk'
	expiration = datetime.timedelta(days=5)
	mocker.patch('app.fb_user.FbUser.login_user',return_value= (mock_cookie, expiration))
	cookie, _ = User.login_user('mock_token')
	assert cookie == mock_cookie


def test_user_add_organization(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	User.add_user('agustin','agustin.payaslian@gmail.com')
	user = User.get_user_by_mail('agustin.payaslian@gmail.com')
	org_name = "Accenture"
	orga_name = user.create_organization(org_name, 'asdad')
	assert orga_name == org_name
	User.delete_user_with_mail('agustin.payaslian@gmail.com')


def test_user_get_organization(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	User.add_user('agustin','agustin.payaslian@gmail.com')
	user = User.get_user_by_mail('agustin.payaslian@gmail.com')
	user.create_organization('Accentur','wwdasdasf')
	orgas = user.get_organizations()
	assert 'Accentur' in orgas[1].values()
	assert 'wwdasdasf' in orgas[1].values()
	User.delete_user_with_mail('agustin.payaslian@gmail.com')

