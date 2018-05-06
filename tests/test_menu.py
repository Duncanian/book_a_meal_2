import json
import unittest
from .test_config import GroundTests


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

        # Add meals to menu
        self.add_menu_data = {
            "meal_ids": [1, 2, 3],
            "menu_name": "Labour"
        }

        # Add none existing meal to menu
        self.wrong_data = {
            "meal_ids": [8, 6, 5],
            "menu_name": "Labour"
        }

        # Add empty meal ids to menu
        self.empty_ids = {
            "meal_ids": [],
            "menu_name": "Labour"
        }

        # Add wrong input type to menu
        self.wrong_input_data = {
            "meal_ids": "wrong",
            "menu_name": "Labour"
        }

        # Add empty menu name
        self.empty_name = {
            "meal_ids": [1, 2, 3],
            "menu_name": ""
        }

        # Add wrong input type to menu name
        self.wrong_input_name = {
            "meal_ids": [1, 2, 3],
            "menu_name": 12
        }

        # Add spaces in menu name
        self.spaces_name = {
            "meal_ids": [1, 2, 3],
            "menu_name": "Labour     "
        }

        # Add different inputs in meal ids list
        self.meal_ids_test = {
            "meal_ids": [1, 2, '3'],
            "menu_name": "Labour"
        }

    def tearDown(self):
        GroundTests.tearDown(self)

    def test_wrong_fields_in_add_menu(self):
        '''Test if one enters no field, one field or more than two fields'''
        response = self.tester.post(
            '/api/v2/menu/', data=json.dumps(self.no_field), headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please ensure that you have Meal ids and Menu Name fields')

        response = self.tester.post(
            '/api/v2/menu/', data=json.dumps(self.one_field), headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please ensure that you have Meal ids and Menu Name fields')

        response = self.tester.post(
            '/api/v2/menu/', data=json.dumps(self.more_fields), headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please ensure that you have Meal ids and Menu Name fields')

    def test_meal_empty_list(self):
        '''Check if meal ids are empty'''
        response = self.tester.post(
            '/api/v2/menu/', data=json.dumps(self.empty_ids), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], "Please enter an id to add your meals to the menu")

    def test_wrong_input_type(self):
        '''Check if meal ids are empty'''
        response = self.tester.post(
            '/api/v2/menu/', data=json.dumps(self.wrong_input_data), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], "Please enter list id values for meals")

    def test_meal_ids_input_types(self):
        '''Check if meal ids should only be integers'''
        response = self.tester.post(
            '/api/v2/menu/', data=json.dumps(self.meal_ids_test), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], "List values should only be in numbers")

    def test_if_meal_doesnt_exists(self):
        '''Check if meal is not available'''
        response = self.tester.post(
            '/api/v2/menu/', data=json.dumps(self.wrong_data), headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "The meal was not found")

    def test_empty_menu_name(self):
        '''Check if menu name is empty'''
        response = self.tester.post(
            '/api/v2/menu/', data=json.dumps(self.empty_name), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Please enter the Menu name")

    def test_wrong_input_menu_name(self):
        '''Check for wrong input other than string'''
        response = self.tester.post(
            '/api/v2/menu/', data=json.dumps(self.wrong_input_name), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], "Please enter a string value for Menu name")

    def test_spaces_in_menu_name(self):
        '''Check for spaces in meal name'''
        response = self.tester.post(
            '/api/v2/menu/', data=json.dumps(self.spaces_name), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Menu name should not have spaces!")

    def test_add_menu_success(self):
        '''Check if the menu is created successfully'''
        response = self.tester.post(
            '/api/v2/menu/', data=json.dumps(self.add_menu_data), headers=self.headers)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "New meal added to the menu!")

    def test_menu_exists(self):
        '''Check if the menu exists'''
        response = self.tester.post(
            '/api/v2/menu/', data=json.dumps(self.add_menu_data), headers=self.headers)
        self.assertEqual(response.status_code, 201)

        response1 = self.tester.post(
            '/api/v2/menu/', data=json.dumps(self.add_menu_data), headers=self.headers)
        self.assertEqual(response1.status_code, 400)
        data = json.loads(response1.data)
        self.assertEqual(data['message'], "Menu already available!")

    def test_user_views(self):
        '''Check if user can view the menu'''
        response = self.tester.post(
            '/api/v2/menu/', data=json.dumps(self.add_menu_data), headers=self.headers)
        self.assertEqual(response.status_code, 201)

        response = self.tester.get('/api/v2/menu/', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data['data'], list, msg='Incorrect output type')


if __name__ == "__main__":
    unittest.main()
