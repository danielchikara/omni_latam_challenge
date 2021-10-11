from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from api.models import *
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
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.test_login_user())
        response = self.client.get('/api/detail/client/')
        result = json.loads(response.content)
        self.assertIn('user', result)

    def test_update_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.test_login_user())
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
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.test_login_user())
        response = self.client.post('/api/logout/client/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProductTestCase(TestCase):
    def setUp(self):
        user = User(
            email='user@test.com',
            first_name='Testing',
            last_name='Testing',
        )
        user.set_password('rc{4@qHjR>!b`yAV')
        user.save()
        self.user = user

        user_admin = User(
            email='admin@test.com',
            first_name='Testing',
            last_name='Testing',
        )
        user_admin.set_password('rc{4@qHjR>!b`yAV')
        user_admin.is_staff = True
        user_admin.is_superuser = True
        user_admin.save()
        self.user_admin = user_admin

        product = Product(
            product_name='producto test 1',
            price=1234,

        )
        self.client = APIClient()

    def login(self, is_admin):
        if is_admin:
            email = self.user_admin.email
        else:
            email = self.user.email
        response = self.client.post('/api/login/client/', {
            'email': email,
            'password': 'rc{4@qHjR>!b`yAV'
        },
            format='json'
        )
        result = json.loads(response.content)
        return result['token']

    def test_product_create(self):
        print(self.login(is_admin=True))
        #print (token)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login(is_admin=True))
        response = self.client.post('/api/create/product/', {
            'product_name': 'producto test 2',
            'price': '5400.25655',

        },
            format='json'
        )
        print(response)
        product = json.loads(response.content)
        print(product)
