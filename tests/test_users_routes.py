from app import app
import json
import pytest
from pytest_mock import mocker
from firebase_admin import auth
import datetime


def test_correct_register(mocker):
	
	with app.test_client() as client:
		mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
		mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
		user = {
			'name':'agustin',
			'mail':'agustin.payaslian@gmail.com'
			}
		response = client.post('/register', data=json.dumps(user),  content_type='application/json')
		mensaje = response.get_json()
		assert response.status_code == 200
		assert 'added' in mensaje['message']
		client.delete('/deleteone', data=json.dumps(user),  content_type='application/json')
	

def test_invalid_mail_register(mocker):
	
	with app.test_client() as client:
		user = {
			'name':'agustin',
			'mail':'payas17hotmail.com'
		}
		response = client.post('/register', data=json.dumps(user),  content_type='application/json')
		mensaje = response.get_json()
		assert response.status_code == 400
		assert 'Invalid' in mensaje['message']


def test_alredy_regitered_mail_register(mocker):
	
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)

	with app.test_client() as client:
		user = {
			'name':'agustin',
			'mail':'payas17@hotmail.com'
		}
		response = client.post('/register', data=json.dumps(user),  content_type='application/json')
		response = client.post('/register', data=json.dumps(user),  content_type='application/json')
		mensaje = response.get_json()
		assert response.status_code == 400
		assert 'registered' in mensaje['message']
		client.delete('/deleteone', data=json.dumps(user),  content_type='application/json')


def test_login(mocker):
	
	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }

	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
	mocker.patch('app.fb_user.FbUser.login_user',return_value= ('mock_cookie', 'expiration'))
	
	with app.test_client() as client:
		user = {
			'name':'agustin',
			'mail':'payas17@hotmail.com'
		}
		token = {'token': 'sarasa'}
		response = client.post('/register', data=json.dumps(user),  content_type='application/json')
		response = client.post('/login', data=json.dumps(token),  content_type='application/json')
		mensaje = response.get_json()
		assert response.status_code == 200
		assert 'logged' in mensaje['message']
		client.delete('/deleteone', data=json.dumps(user),  content_type='application/json')


# def test_logout(mocker):
	
# 	mock_user={'name': 'agustin', 'mail': 'agustin.payaslian@gmail.com' }
# 	mock_cookie = 'ksgdfhgs<hgfskjfgjksgfkjsgfjsgfjksdgfk'

# 	mocker.patch('app.fb_user.FbUser.get_user_by_email',return_value=mock_user)
# 	mocker.patch('app.fb_user.FbUser.login_user',return_value= (mock_cookie, 'expiration'))
	
# 	with app.test_client() as client:
# 		user = {
# 			'name':'agustin',
# 			'mail':'payas17@hotmail.com'
# 		}
# 		token = {'token': 'sarasa'}
# 		response = client.post('/register', data=json.dumps(user),  content_type='application/json')
# 		response = client.post('/login', data=json.dumps(token),  content_type='application/json')
# 		mensaje = response.get_json()
# 		response = client.post('/logout')
# 		mensaje = response.get_json()
# 		assert response.status_code == 200
# 		assert 'out' in mensaje['message']
# 		client.delete('/deleteone', data=json.dumps(user),  content_type='application/json')
	



