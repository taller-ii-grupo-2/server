from app.users import User
from app.exceptions import InvalidMail, SignedMail, InvalidToken, UserNotRegistered
from firebase_admin import auth
import pytest
import datetime


# def test_addusers_incorrect_mail():
	
# 	with pytest.raises(InvalidMail):
# 		User.add_user('agustin','agustin.payasliangmail.com')
# 	User.delete_all()
	

# def test_addusers_correct_mail():

# 	user = auth.create_user(
#     email='agustin.payaslian@gmail.com',
#     password='secretPassword',
#     display_name='agustin')
# 	User.add_user('agustin','agustin.payaslian@gmail.com')
# 	user = User.get_user_by_mail('agustin.payaslian@gmail.com')
# 	assert 'agustin' in user.name
# 	User.delete_user_with_mail('agustin.payaslian@gmail.com')


# def test_addusers_with_same_mail():
# 	user = auth.create_user(
#     email='agustin.payaslian@gmail.com',
#     password='secretPassword',
#     display_name='agustin')
# 	User.add_user('agustin','agustin.payaslian@gmail.com')
# 	with pytest.raises(SignedMail):
# 		User.add_user('agustin','agustin.payaslian@gmail.com')
# 	User.delete_user_with_mail('agustin.payaslian@gmail.com')

# def test_addusers_not_signed_in_firebase():
# 	with pytest.raises(UserNotRegistered):
# 		User.add_user('agustin','agustin.payaslian@gmail.com')

# def test_incorrect_login_user():

# 	with pytest.raises(InvalidToken):
# 		User.login_user('asdads')

# def test_correct_login_user():

# 	# user = auth.create_user(
#  #    email='agustin.payaslian@gmail.com',
#  #    password='secretPassword',
#  #    display_name='agustin')
# 	# User.add_user('agustin','agustin.payaslian@gmail.com')
# 	# expiration = datetime.timedelta(days=5)
# 	# cookie = User.login_user(user.uid, expiration)
# 	# User.delete_user_with_mail('agustin.payaslian@gmail.com')

# 	user = auth.get_user('dT2vZ1A6kGhl6H0vcwaN7Lans052')
# 	assert user.email == 'turi@gmail.com'



