from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from api.models import User
import json

# Create your tests here.

class UserTestCase(TestCase):
    def setUp(self):
        user ={ 
            'email':'testing_login@cosasdedevs.com',
            'first_name':'Testing',
            'last_nam':'Testing',
            'password' : 'rc{4@qHjR>!b`yAV'
            }
        #user.set_password('rc{4@qHjR>!b`yAV')
        #user.save()
    
    def test_signup_user(self):
        client = APIClient()
        response = client.post(
                '/api/register/client/', {
                'first_name': 'Testing',
                'last_name': 'Testing',
                'email': 'testing_login@cosasdedevs.com',
                'password': 'rc{4@qHjR>!b`yAV',

            },
            format='multipart'
        )
        print(response,"aaaaaaaa")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'success': True})

