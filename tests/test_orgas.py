from app.users import User
from app.organizations import Organization
from app.messages import Message
import pytest
from app.exceptions import InvalidOrganizationName, UserIsAlredyInOrganization
from app.exceptions import AlreadyCreatedChannel, InvalidOrganization
from app.exceptions import SignedOrganization, UserNotInOrganization, UserIsAlreadyAdmin

def test_addorgas_too_long_name():
	org_name = "Rs4hi5zVr9TVHilIPTOCPPRqOvBIuPOnl"
	with pytest.raises(InvalidOrganizationName):
		Organization.add_orga(org_name,'asdad',1)

def test_get_organization_that_does_not_exist():
	with pytest.raises(InvalidOrganization):
		Organization.get_organization_by_name('namdadasd')

def test_get_organization_that_exists():
	Organization.add_orga('name','asdad',1)
	Organization.get_organization_by_name('name')

def test_addorgas_correctly():
	org_name = "Exxon mobile"
	orga = Organization.add_orga(org_name, 'www.asd.com',1)
	assert org_name == orga.name

def test_add_signedOrga(mocker):
	with pytest.raises(SignedOrganization):
		orga = Organization.add_orga('org_name', 'www.asd.com',1)
		orga = Organization.add_orga('org_name', 'www.asd.com',1)
	
def test_orgas_add_users(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com'}
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com')
	org_name = "Exxon mobile"
	orga = Organization.add_orga(org_name, 'www.asd.com',user.id)
	orga.add_user(user)
	assert len(orga.users) == 1

def test_orgas_create(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com'}
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com')
	org_name = "Exxon mobile"
	orga = Organization.create(org_name, 'www.asd.com',user)
	assert len(orga.users) == 1
	assert len(orga.channels) == 2


def test_orgas_add_channel(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com'}
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com')
	org_name = "Exxon mobile"
	orga = Organization.add_orga(org_name, 'www.asd.com',user.id)
	orga.add_user(user)
	orga.create_channel('asd',False,user,'sad','asd')
	assert len(orga.channels) == 1

def test_add_the_same_user_twice(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com'}
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com')
	org_name = "Exxon mobile"
	orga = Organization.add_orga(org_name, 'www.asd.com',user.id)
	orga.add_user(user)
	with pytest.raises(UserIsAlredyInOrganization):
		orga.add_user(user)

def test_orgas_add_two_channels_with_same_name(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com')
	org_name = "Exxon mobile"
	orga = Organization.create(org_name, 'www.asd.com',user)
	with pytest.raises(AlreadyCreatedChannel):
		orga.create_channel('asd',False,user,'sad','asd')
		orga.create_channel('asd',False,user,'sad','asd')

def test_create_orga_and_add_channels(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com'}
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com')
	org_name = "Exxon mobile"
	orga = Organization.create(org_name, 'www.asd.com',user)
	orga.create_channel('asd',False,user,'sad','asd')
	assert len(orga.channels) == 3

def test_add_user(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com')
	user2 = User.add_user('agustin','payas17@gmail.com')
	org_name = "Exxon mobile"
	orga = Organization.create(org_name, 'www.asd.com',user)
	orga.add_user(user2)
	assert len(orga.users) == 2

def test_create_channel_with_user_that_doesnt_belong_to_organization(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com')
	user2 = User.add_user('agustin','payas17@gmail.com')
	org_name = "Exxon mobile"
	orga = Organization.create(org_name, 'www.asd.com',user)
	with pytest.raises(UserNotInOrganization):
		orga.create_channel('asd',False,user2,'sad','asd')

def test_get_channels_with_user(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com')
	org_name = "Exxon mobile"
	orga = Organization.create(org_name, 'www.asd.com',user)
	assert len(orga.get_channels_with_user(user.id)) == 2

def test_get_user_in_private_channel(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com')
	user2 = User.add_user('agustin','payas17@gmail.com')
	org_name = "Exxon mobile"
	orga = Organization.create(org_name, 'www.asd.com',user)
	orga.add_user(user2)
	channel = orga.create_channel('asd',True,user2,'sad','asd')
	assert len(channel.users) == 1

def test_get_users_per_channel(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com')
	user2 = User.add_user('agustin','payas17@gmail.com')
	org_name = "Exxon mobile"
	orga = Organization.create(org_name, 'www.asd.com',user)
	orga.add_user(user2)
	channel = orga.create_channel('asd',True,user2,'sad','asd')
	assert len(orga.get_channels_with_user(user.id)) == 2
	assert len(orga.get_channels_with_user(user2.id)) == 3


def test_create_channel_then_add_user(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com')
	user2 = User.add_user('agustin','payas17@gmail.com')
	org_name = "Exxon mobile"
	orga = Organization.create(org_name, 'www.asd.com',user)
	channel = orga.create_channel('asd',False,user,'sad','asd')
	orga.add_user(user2)
	assert len(orga.get_channels_with_user(user.id)) == 3
	assert len(orga.get_channels_with_user(user2.id)) == 3

def test_create_private_channel_then_add_user(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com')
	user2 = User.add_user('agustin','payas17@gmail.com')
	org_name = "Exxon mobile"
	orga = Organization.create(org_name, 'www.asd.com',user)
	channel = orga.create_channel('asd',True,user,'sad','asd')
	orga.add_user(user2)
	assert len(orga.get_channels_with_user(user.id)) == 3
	assert len(orga.get_channels_with_user(user2.id)) == 2

def test_add_users_per_channel(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com')
	user2 = User.add_user('agustin','payas17@gmail.com')
	org_name = "Exxon mobile"
	orga = Organization.create(org_name, 'www.asd.com',user)
	orga.add_user(user2)
	channel = orga.create_channel('asd',True,user2,'sad','asd')
	orga.add_user_to_channel(user,channel.name)
	assert len(orga.get_channels_with_user(user.id)) == 3
	assert len(orga.get_channels_with_user(user2.id)) == 3

def test_add_admin_that_is_not_user(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com')
	org_name = "Exxon mobile"
	orga = Organization.add_orga(org_name, 'www.asd.com',1)
	with pytest.raises(UserNotInOrganization):
		orga.add_admin(user)

def test_add_admin(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com')
	org_name = "Exxon mobile"
	orga = Organization.add_orga(org_name, 'www.asd.com',1)
	orga.add_user(user)
	orga.add_admin(user)
	assert user in orga.admins

def test_add_admin_and_user(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com')
	org_name = "Exxon mobile"
	orga = Organization.add_orga(org_name, 'www.asd.com',1)
	orga.add_user_admin(user)
	assert user in orga.admins

def test_create_orga_with_admin_user(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com')
	org_name = "Exxon mobile"
	orga = Organization.create(org_name, 'www.asd.com',user)
	assert user in orga.admins

def test_add_admin_to_admin(mocker):
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	user = User.add_user('agustin','agustin.payaslian@gmail.com')
	org_name = "Exxon mobile"
	orga = Organization.create(org_name, 'www.asd.com',user)
	with pytest.raises(UserIsAlreadyAdmin):
		orga.add_admin(user)
