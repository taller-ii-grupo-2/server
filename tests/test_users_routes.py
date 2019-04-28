from app import app
import json
import pytest
from firebase_admin import auth


def test_correct_register():
	
	with app.test_client() as client:
		fb_user = auth.create_user(
	    email='agustin.payaslian@gmail.com',
	    password='secretPassword',
	    display_name='agustin')
		user = {
			'name':'agustin',
			'mail':'agustin.payaslian@gmail.com'
			}
		response = client.post('/register', data=json.dumps(user),  content_type='application/json')
		mensaje = response.get_json()
		assert response.status_code == 200
		assert 'added' in mensaje['message']
		client.delete('/deleteone', data=json.dumps(user),  content_type='application/json')
	

def test_invalid_mail_register():
	
	with app.test_client() as client:
		user = {
			'name':'agustin',
			'mail':'payas17hotmail.com'
		}
		response = client.post('/register', data=json.dumps(user),  content_type='application/json')
		mensaje = response.get_json()
		assert response.status_code == 400
		assert 'Invalid' in mensaje['message']


def test_alredy_regitered_mail_register():
	
	fb_user = auth.create_user(
	    email='payas17@hotmail.com',
	    password='secretPassword',
	    display_name='agustin')

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
	



