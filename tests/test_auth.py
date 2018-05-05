import json
import unittest
import uuid
from .test_config import GroundTests
from models.models import User


class TestAuth(GroundTests):
    def setUp(self):
        GroundTests.setUp(self)
        # Register details
        self.registerdata = {
            "username": "three",
            "password": "#2345",
            "admin": False
        }

        # A missing detail in register details
        self.reg_miss_data = {
            "username": "",
            "password": "#2345",
            "admin": False
        }

        # Wrong inputs for register
        self.reg_bad_data = {
            "username": 123,
            "password": 45,
            "admin": False
        }

        # Username having spaces for register
        self.reg_space_data = {
            "username": "       ",
            "password": "sdfb ",
            "admin": False
        }

        # Password having less than 5 chars register
        self.reg_less_data = {
            "username": "jbnjn",
            "password": "sdf",
            "admin": False
        }

        # Password having more than 10 chars register
        self.reg_more_data = {
            "username": "wuytg",
            "password": "jbnjngygvvsgshsjsbsudbduxh",
            "admin": False
        }

        # Login details
        self.u_data = {
            "username": "ian",
            "password": "#2345"
        }

        # Wrong/Non-existence login details
        self.u_err_data = {
            "username": "dan",
            "password": "2345"
        }

        # Empty login details
        self.u_emt_data = {
            "username": "",
            "password": "#2345"
        }

        # Wrong input types login details
        self.u_bad_data = {
            "username": 123,
            "password": 78
        }

        # Wrong password login details
        self.u_wrong = {
            "username": 'ian',
            "password": '#23456'
        }

    def tearDown(self):
        GroundTests.tearDown(self)

    def test_register(self):
        '''Test for successful register of a user'''
        response = self.tester.post(
            '/api/v2/auth/signup', data=json.dumps(self.registerdata), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'New user created!')

    def test_if_user_is_registered_already(self):
        '''Test if the user has an account already'''
        response = self.tester.post(
            '/api/v2/auth/signup', data=json.dumps(self.u_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Sorry, username already taken!')

    def test_users(self):
        response = self.tester.get('/api/v2/users', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data['data'], list, msg='Incorrect output type')

    def test_register_blank(self):
        '''Test for error when an input is left blank'''
        response = self.tester.post(
            '/api/v2/auth/signup', data=json.dumps(self.reg_miss_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Please enter all the details')

    def test_register_wrong_data_type(self):
        '''Test for error when an input is not a string'''
        response = self.tester.post(
            '/api/v2/auth/signup', data=json.dumps(self.reg_bad_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please enter a string value for username and password')

    def test_register_spaces_in_username(self):
        '''Test for error when username has spaces'''
        response = self.tester.post(
            '/api/v2/auth/signup', data=json.dumps(self.reg_space_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Username should not have spaces!')

    def test_register_less_chars(self):
        '''Test if password to be set is less than 5  char'''
        response = self.tester.post(
            '/api/v2/auth/signup', data=json.dumps(self.reg_less_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Password should be more than 5 characters')

    def test_register_more_chars(self):
        '''Test if password to be set is more than 10  char'''
        response = self.tester.post('/api/v2/auth/signup', data=json.dumps(self.reg_more_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Password should be less than 10 characters')

    def test_login_success(self):
        response = self.tester.post(
            '/api/v2/auth/login', data=json.dumps(self.u_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data['token'], str, msg='Incorrect output type')

    def test_login_blank(self):
        response = self.tester.post(
            '/api/v2/auth/login', data=json.dumps(self.u_emt_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Please enter all the details')

    def test_login_wrong_data_type(self):
        '''Test for error when an input is not a string'''
        response = self.tester.post(
            '/api/v2/auth/login', data=json.dumps(self.u_bad_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please enter a string value for username and password')

    def test_login_gone_wrong(self):
        response = self.tester.post(
            '/api/v2/auth/login', data=json.dumps(self.u_err_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Please sign up then login')

    def test_wrong_pass_login(self):
        response = self.tester.post(
            '/api/v2/auth/login', data=json.dumps(self.u_wrong), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'wrong password, please try again')


if __name__ == "__main__":
    unittest.main()
