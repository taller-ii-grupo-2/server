from app.users import User
from app.channels import Channel
from app.organizations import Organization
from app.exceptions import InvalidChannelName, InvalidChannel
from app.exceptions import UserIsAlredyInChannel
import pytest


def test_addchannel_too_long_name():
	name = "Rs4hi5zVr9TVHilIPTOCPPRqOvBIuPOnl"
	with pytest.raises(InvalidChannelName):
		Channel.add_channel(name,True,1,'asd','asd',1)


def test_addchannel_correctly():
	channel = Channel.add_channel('asds',True,1,'asd','asd',1)
	assert channel.name == 'asds'


def test_adduser_to_channel_correctly(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')
	user2 = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','payaslian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')
	channel = Channel.add_channel('asds',True,1,'asd','asd',1)
	channel.add_user(user)
	channel.add_user(user2)
	assert len(channel.users) == 2

def test_adduser_two_times_will_raise_exception(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')
	channel = Channel.add_channel('asds',True,1,'asd','asd',1)
	channel.add_user(user)
	with pytest.raises(UserIsAlredyInChannel):
		channel.add_user(user)

def test_get_not_existing_channel():
	with pytest.raises(InvalidChannel):
		Channel.get_channel_with_name('name', 1)

def test_add_users(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')
	user2 = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','payaslian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')
	user3 = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','payasssfsfdlian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')
	users = [user,user2,user3]
	channel = Channel.add_channel('asds',True,1,'asd','asd',1)
	channel.add_users(users)
	assert len(channel.users) == 3

def test_add_users_already_in_channel(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')
	user2 = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','payaslian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')
	user3 = User.add_user('agustin','agustin.payaslian@gmail.com','agustin.payaslian@gmail.com','payasssfsfdlian@gmail.com',3.14,3.14,'agustin.payaslian@gmail.com')
	users = [user,user2,user3,user]
	channel = Channel.add_channel('asds',True,1,'asd','asd',1)
	channel.add_users(users)
	assert len(channel.users) == 3