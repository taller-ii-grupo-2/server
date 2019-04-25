from app.users import User
from app.exceptions import InvalidMail, SignedMail
import pytest
import os
from app import db


def test_addusers_incorrect_mail():
    print(os.environ['DATABASE_URL'])
    with pytest.raises(InvalidMail):
        User.add_user('agustin','agustin.payasliangmail.com','asdasd')
   # User.delete_all()

def test_addusers_correct_mail():
    db.create_all()
    user = User.add_user('agustin','agustin.payaslian@gmail.com','asdasd')
    assert 'agustin' in user.name

# def test_addusers_incorrect_mail():
#     with pytest.raises(InvalidMail):
#         User.add_user('agustin','agustin.payasliangmail.com','asdasd')
#     User.delete_all()
	

# def test_addusers_correct_mail():

# 	user = User.add_user('agustin','agustin.payaslian@gmail.com','asdasd')
# 	assert 'agustin' in user.name
# 	User.delete_all()

# def test_addusers_criptographic_password():
# 	password = 'asdasd'
# 	user = User.add_user('agustin','agustin.payaslian@gmail.com',password)
# 	assert user.password != password
# 	User.delete_all()

# def test_addusers_with_same_mail():
# 	password = 'asdasd'
# 	user = User.add_user('agustin','agustin.payaslian@gmail.com',password)
# 	with pytest.raises(SignedMail):
# 		user = User.add_user('agustin','agustin.payaslian@gmail.com',password)
# 	User.delete_all()


