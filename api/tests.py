from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from api.models import User
import json

# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self):
        user = User(
            email='chikara@test.com',
            first_name='Testing',
            last_name='Testing',
        )
        user.set_password('rc{4@qHjR>!b`yAV')
        user.save()
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.test_login_user())

    def test_register_user(self):
        response = self.client.post(
            '/api/register/client/', {
                'first_name': 'Testing',
                'last_name': 'Testing',
                'email': 'testing@chikara.com',
                'password': 'rc{4@qHjR>!b`yAV',
                'password_confirmation': 'rc{4@qHjR>!b`yAV',
            },
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), {'success': True})

    def test_login_user(self):
        response = self.client.post('/api/login/client/', {
            'email': 'chikara@test.com',
            'password': 'rc{4@qHjR>!b`yAV'
        },
            format='json'
        )
        result = json.loads(response.content)
        self.assertIn('token', result)
        self.access_token = result['token']
        return result['token']

    def test_info_user(self):
        response = self.client.get('/api/info/client/')
        result = json.loads(response.content)
        self.assertIn('user', result)

    def test_update_user(self):
        response = self.client.post('/api/update/client/', {
            'first_name': 'Daniel',
            'last_name': 'chikara',
        },
            format='json'
        )
        result = json.loads(response.content)
        self.assertIn('Daniel', result['user']['first_name'])
        self.assertIn('chikara', result['user']['last_name'])

    def test_logout_user(self):
        response = self.client.post('/api/logout/client/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        