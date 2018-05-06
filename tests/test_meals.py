import json
import unittest
import uuid
from .test_config import GroundTests
from models.models import Meals


class TestMeals(GroundTests):
    def setUp(self):
        GroundTests.setUp(self)
        # No input field
        self.no_field = {

        }

        # One field
        self.one_field = {
            "meal_name": "Chapatti"
        }

        # More than two fields
        self.more_fields = {
            "meal_name": "Chapatti",
            "meal_price": 25,
            "admin": False
        }

        # Add meal
        self.add_meal_data = {
            "meal_name": "Chapatti",
            "meal_price": 25
        }

        # A missing detail in register details
        self.add_miss_data = {
            "meal_name": "",
            "meal_price": 25
        }

        # Wrong data type for meal_name
        self.meal_name_typo = {
            "meal_name": 12,
            "meal_price": 25
        }

        # Wrong data type for meal_price
        self.meal_price_typo = {
            "meal_name": "Chapatti",
            "meal_price": "25"
        }

        # Spaces in meal name
        self.meal_name_space = {
            "meal_name": "Chapatti      ",
            "meal_price": 25
        }
        # Meal exists in db
        self.meal_in_db = {
            "meal_name": "Rice",
            "meal_price": 200
        }

        # Modify meal
        self.modify_meal = {
            "meal_name": "kuku",
            "meal_price": 28
        }

        # Modify meal with empty inputs
        self.mod_emp_meal = {
            "meal_name": "",
            "meal_price": 28
        }

        # Modify meal with meal name not string
        self.mod_int_meal = {
            "meal_name": 1234567,
            "meal_price": 28
        }

        # Modify meal with meal price not integer
        self.mod_str_price = {
            "meal_name": "1234567",
            "meal_price": "28"
        }

        # Modify meal with meal name having spaces
        self.mod_space_meal = {
            "meal_name": "  1234567   ",
            "meal_price": 28
        }

    def tearDown(self):
        GroundTests.tearDown(self)

    def test_add_meal(self):
        '''Add meal successfully to db'''
        response = self.tester.post(
            '/api/v2/meals/', data=json.dumps(self.add_meal_data), headers=self.headers)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'New meal added!')

    def test_wrong_fields_in_add_meal(self):
        '''Test if one enters no field, one field or more than two fields'''
        response = self.tester.post(
            '/api/v2/meals/', data=json.dumps(self.no_field), headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please ensure that you have only Meal Name and Meal Price fields')

        response = self.tester.post(
            '/api/v2/meals/', data=json.dumps(self.one_field), headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please ensure that you have only Meal Name and Meal Price fields')

        response = self.tester.post(
            '/api/v2/meals/', data=json.dumps(self.more_fields), headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please ensure that you have only Meal Name and Meal Price fields')

    def test_missing_data_in_input(self):
        '''Check if empty data will go through'''
        response = self.tester.post(
            '/api/v2/meals/', data=json.dumps(self.add_miss_data), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Please enter all the details')

    # def test_type_of_meal_name(self):
    #     '''Check if meal to be added is a string'''
    #     response = self.tester.post('/api/v2/meals/', data=json.dumps(self.meal_name_typo), headers=self.headers)
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data)
    #     print(data)
    #     self.assertEqual(data['message'], 'Please enter a string value for meal name')

    def test_type_of_meal_price(self):
        '''Check if meal price is an integer'''
        response = self.tester.post(
            '/api/v2/meals/', data=json.dumps(self.meal_price_typo), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Price should be a number')

    def test_spaces_meal_name(self):
        '''Check if meal has spaces in it'''
        response = self.tester.post(
            '/api/v2/meals/', data=json.dumps(self.meal_name_space), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Meal name should not have spaces!')

    def test_meal_existing_in_db(self):
        '''Check if meal exists in db'''
        response = self.tester.post(
            '/api/v2/meals/', data=json.dumps(self.meal_in_db), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'The meal already exists')

    def test_get_meals(self):
        '''Check if meal data is available'''
        response = self.tester.get('/api/v2/meals/', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data['data'], list, msg='Incorrect output type')

    def test_doesnt_meal_exists(self):
        '''Check if meal doesn't exists in db'''
        response = self.tester.put(
            '/api/v2/meals/7', data=json.dumps(self.modify_meal), headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "The meal was not found")

    def test_empty_inputs_in_put(self):
        '''Check if some inputs are empty'''
        response = self.tester.put(
            '/api/v2/meals/1', data=json.dumps(self.mod_emp_meal), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Please enter all the details')

    def test_meal_name_not_string(self):
        '''Check if meal name is not a string'''
        response = self.tester.put(
            '/api/v2/meals/1', data=json.dumps(self.mod_int_meal), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please enter a string value for meal')

    def test_meal_price_not_integer(self):
        '''Check if meal name is not a string'''
        response = self.tester.put(
            '/api/v2/meals/1', data=json.dumps(self.mod_str_price), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please enter a number value for price')

    def test_meal_name_having_spaces(self):
        '''Check if meal name has spaces'''
        response = self.tester.put(
            '/api/v2/meals/1', data=json.dumps(self.mod_space_meal), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Meal name should not have spaces!')

    def test_modified_success(self):
        '''Check for successful meal modification'''
        response = self.tester.put(
            '/api/v2/meals/1', data=json.dumps(self.modify_meal), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['data'], 'Meal modified!')

    def test_delete_when_meal_unavailable(self):
        '''Check presence of meal to be deleted'''
        response = self.tester.delete('/api/v2/meals/9', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "The meal was not found")

    def test_delete_success(self):
        '''Check for successful deletion of meal'''
        response = self.tester.delete('/api/v2/meals/1', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "The meal has been deleted")


if __name__ == "__main__":
    unittest.main()
