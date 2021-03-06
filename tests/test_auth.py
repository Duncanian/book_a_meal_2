import json
import unittest
import uuid
from .test_config import GroundTests
from models.models import User


class TestAuth(GroundTests):
    def setUp(self):
        GroundTests.setUp(self)
        # No input field
        self.no_field = {

        }

        # One field
        self.one_field = {
            "username": "three"
        }

        # Two fields
        self.two_fields = {
            "username": "three",
            "password": "#2345"
        }

        # More than two fields
        self.more_fields = {
            "username": "three",
            "email": "ian@test.com",
            "password": "#2345",
            "admin": False
        }

        # Register details
        self.registerdata = {
            "username": "three",
            "email": "ian@test.com",
            "password": "#2345"
        }

        # Existing user details
        self.exist_reg_data = {
            "username": "ian",
            "email": "ian@test.com",
            "password": "#2345"
        }

        # A missing detail in register details
        self.reg_miss_data = {
            "username": "",
            "email": "ian@test.com",
            "password": "#2345"
        }

        # Wrong inputs for register
        self.reg_bad_data = {
            "username": 123,
            "email": "ian@test.com",
            "password": 45
        }

        # Username having spaces for register
        self.reg_space_data = {
            "username": "       ",
            "email": "ian@test.com",
            "password": "sdfb "
        }

        # Password having less than 5 chars register
        self.reg_less_data = {
            "username": "jbnjn",
            "email": "ian@test.com",
            "password": "sdf"
        }

        # Password having spaces for register
        self.reg_space_data2 = {
            "username": "ian234",
            "email": "ian@test.com",
            "password": "         "
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

        # Empty profile ID field
        self.no_profile = {

        }

        # More fields on profile
        self.more_profile = {
            "u_id": 123,
            "password": 78
        }

        # Non existence profile ID
        self.non_existent_profile = {
            "u_id": 456
        }

        # Correct profile ID
        self.profile = {
            "u_id": 1
        }

        # Wrong profile ID input
        self.wrong_profile = {
            "u_id": "1"
        }

    def tearDown(self):
        GroundTests.tearDown(self)

    def test_wrong_fields_in_signup(self):
        '''Test if one enters no field, one field or more than two fields'''
        response = self.tester.post(
            '/api/v2/auth/signup', data=json.dumps(self.no_field), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please ensure that you have only Username, Email and Password fields')

        response = self.tester.post(
            '/api/v2/auth/signup', data=json.dumps(self.one_field), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please ensure that you have only Username, Email and Password fields')

        response = self.tester.post(
            '/api/v2/auth/signup', data=json.dumps(self.two_fields), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please ensure that you have only Username, Email and Password fields')

        response = self.tester.post(
            '/api/v2/auth/signup', data=json.dumps(self.more_fields), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please ensure that you have only Username, Email and Password fields')

    def test_register(self):
        '''Test for successful register of a user'''
        response = self.tester.post(
            '/api/v2/auth/signup', data=json.dumps(self.registerdata), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'You have been successfully registered!')
        self.assertIsInstance(data['data'], dict, msg='Incorrect output type')

    def test_if_user_is_registered_already(self):
        '''Test if the user has an account already'''
        response = self.tester.post(
            '/api/v2/auth/signup', data=json.dumps(self.exist_reg_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
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
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Please enter all the details')

    def test_register_wrong_data_type(self):
        '''Test for error when an input is not a string'''
        response = self.tester.post(
            '/api/v2/auth/signup', data=json.dumps(self.reg_bad_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please enter a string value for username, email and password')

    def test_register_spaces_in_username(self):
        '''Test for error when username has spaces'''
        response = self.tester.post(
            '/api/v2/auth/signup', data=json.dumps(self.reg_space_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Username should not have spaces!')

    def test_register_less_chars(self):
        '''Test if password to be set is less than 5  char'''
        response = self.tester.post(
            '/api/v2/auth/signup', data=json.dumps(self.reg_less_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Password should be more than 5 characters')

    def test_register_spaces_in_password(self):
        '''Test for error when password has spaces'''
        response = self.tester.post(
            '/api/v2/auth/signup', data=json.dumps(self.reg_space_data2), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Password should not have spaces!')

    def test_normal_user_doesnt_exists(self):
        '''Check if normal user doesn't exists in db'''
        response = self.tester.put(
            '/api/v2/auth/make_admin/4/', data=json.dumps({"admin": True}), headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "No such user found")

    def test_type_of_admin_value(self):
        '''Check wrong type of admin value'''
        response = self.tester.put(
            '/api/v2/auth/make_admin/2/', data=json.dumps({"admin": 12}), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please enter a boolean value for admin')

    def test_success_make_admin(self):
        '''Check for successful making of admin'''
        response = self.tester.put(
            '/api/v2/auth/make_admin/2/', data=json.dumps({"admin": True}), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'User successfully made an admin')

    def test_wrong_fields_in_login(self):
        '''Test if one enters no field, one field or more than two fields'''
        response = self.tester.post(
            '/api/v2/auth/login', data=json.dumps(self.no_field), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please ensure that you have only Username and Password fields')

        response = self.tester.post(
            '/api/v2/auth/login', data=json.dumps(self.one_field), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please ensure that you have only Username and Password fields')

        response = self.tester.post(
            '/api/v2/auth/login', data=json.dumps(self.more_fields), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please ensure that you have only Username and Password fields')

    def test_login_success(self):
        response = self.tester.post(
            '/api/v2/auth/login', data=json.dumps(self.u_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIsInstance(data['token'], str, msg='Incorrect output type')

    def test_login_blank(self):
        response = self.tester.post(
            '/api/v2/auth/login', data=json.dumps(self.u_emt_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Please enter all the details')

    def test_login_wrong_data_type(self):
        '''Test for error when an input is not a string'''
        response = self.tester.post(
            '/api/v2/auth/login', data=json.dumps(self.u_bad_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please enter a string value for username and password')

    def test_login_gone_wrong(self):
        response = self.tester.post(
            '/api/v2/auth/login', data=json.dumps(self.u_err_data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Please sign up then login')

    def test_wrong_pass_login(self):
        response = self.tester.post(
            '/api/v2/auth/login', data=json.dumps(self.u_wrong), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'wrong password, please try again')


if __name__ == "__main__":
    unittest.main()
