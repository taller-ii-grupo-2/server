from app.users import User
from app.organizations import Organization
from app.exceptions import InvalidMail, SignedMail, InvalidToken, UserNotRegistered, UserIsNotAdmin, UserIsNotCreator
from firebase_admin import auth
import pytest
from pytest_mock import mocker
import os
from app import db
import datetime


def test_addusers_incorrect_mail():
    with pytest.raises(InvalidMail):
        user = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','agustin.payaslianmail.com',3.14,3.14,'agustin.payaslian@gmail.com')
	

def test_addusers_correct_mail(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')
	user = User.get_user_by_mail('agustin.payaslian@gmail.com')
	assert 'agustin' in user.name
	

def test_addusers_with_same_mail(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')
	with pytest.raises(SignedMail):
		user = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')

def test_addusers_not_signed_in_firebase(mocker):
	mocker.patch('app.fb_user.FbUser.get_user_by_email',side_effect= UserNotRegistered )
	with pytest.raises(UserNotRegistered):
		user = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')

def test_incorrect_login_user():

	with pytest.raises(InvalidToken):
		User.login_user('asdads')

def test_correct_login_user(mocker):
	mock_cookie = 'ksgdfhgs<hgfskjfgjksgfkjsgfjsgfjksdgfk'
	expiration = datetime.timedelta(days=5)
	mocker.patch('app.fb_user.FbUser.login_user',return_value= (mock_cookie, expiration))
	cookie, _ = User.login_user('mock_token')
	assert cookie == mock_cookie

def test_user_get_organization(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')
	orga = Organization.create('org_name', 'www.asd.com',user,
                                     'desc','welcome_message')
	orgas = user.get_organizations()
	assert 'org_name' in orgas[0].values()
	assert 'www.asd.com' in orgas[0].values()

def test_user_add_admin_to_organization(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')
	user2 = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','payaslian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')
	orga = Organization.create('org_name', 'www.asd.com',user,
                                     'desc','welcome_message')
	orga.add_user(user2)
	user.make_admin_user(user2,orga)
	assert len(orga.admins) == 2

def test_user_add_admin_to_organization_without_being_admin(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')
	user2 = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','payaslian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')
	user3 = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','payasssfsfdlian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')
	orga = Organization.create('org_name', 'www.asd.com',user,
                                     'desc','welcome_message')
	orga.add_user(user2)
	orga.add_user(user3)
	with pytest.raises(UserIsNotCreator):
		user2.make_admin_user(user3,orga)

def test_total_amount_of_users(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')
	user = User.add_user('agustin','payas17@hotmail.com','payas17@hotmail.com','payas17@hotmail.com',3.14,3.14,'payas17@hotmail.com')
	count = User.amount()
	assert count == 2

