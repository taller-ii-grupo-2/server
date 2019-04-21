from app import app
import json
import pytest


def test_correct_register():
	
	with app.test_client() as client:
		user = {
			'name':'agustin',
			'mail':'payas17@hotmail.com',
			'password': 'asdasd'
		}
		response = client.post('/register', data=json.dumps(user),  content_type='application/json')
		assert response.status_code == 200
		client.delete('/delete')
	

def test_invalid_mail_register():
	
	with app.test_client() as client:
		user = {
			'name':'agustin',
			'mail':'payas17hotmail.com',
			'password': 'asdasd'
		}
		response = client.post('/register', data=json.dumps(user),  content_type='application/json')
		assert response.status_code == 400
	client.delete('/delete')


def test_alredy_regitered_mail_register():
	
	with app.test_client() as client:
		user = {
			'name':'agustin',
			'mail':'payas17@hotmail.com',
			'password': 'asdasd'
		}
		response = client.post('/register', data=json.dumps(user),  content_type='application/json')
		response = client.post('/register', data=json.dumps(user),  content_type='application/json')
		assert response.status_code == 400
	client.delete('/delete')


