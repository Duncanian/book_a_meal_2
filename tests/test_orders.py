import json
import unittest
from .test_config import GroundTests


class TestMeals(GroundTests):
    def setUp(self):
        GroundTests.setUp(self)

        # No input field
        self.no_field = {

        }

        # More than two fields
        self.more_fields = {
            "meal_name": "Chapatti",
            "meal_price": 25
        }

        # Add meals to menu
        self.add_menu_data = {
            "meal_ids": [1, 2, 3],
            "menu_name": "Labour"
        }

        # Add meals to order
        self.add_order_data = {
            "meal_ids": [1, 2, 3]
        }

        # Add none existing meal to order
        self.wrong_data = {
            "meal_ids": [8, 6, 5]
        }

        # Add empty meal ids to order
        self.empty_ids = {
            "meal_ids": []
        }

        # Add wrong input type to order
        self.wrong_input_data = {
            "meal_ids": "wrong"
        }

        # Enter correct qty
        self.qty = {
            'quantity': 3
        }

        # Enter zero or negative qty
        self.neg_qty = {
            'quantity': -3
        }

        # Enter empty qty
        self.empty_qty = {
            'quantity': ''
        }

        # Enter wrong input qty
        self.wrong_qty = {
            'quantity': '3'
        }

        # Add different inputs in meal ids list
        self.meal_ids_test = {
            "meal_ids": [1, 2, '3']
        }

        # Add negative meal ids
        self.meal_ids_neg = {
            "meal_ids": [1, 2, -3]
        }

        self.tester.post(
            '/api/v2/menu/', data=json.dumps(self.add_menu_data), headers=self.headers)

    def tearDown(self):
        GroundTests.tearDown(self)

    def test_wrong_fields_in_add_menu(self):
        '''Test if one enters no field, one field or more than two fields'''
        response = self.tester.post(
            '/api/v2/orders/', data=json.dumps(self.no_field), headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please ensure that you have only a Meal ids field')

        response = self.tester.post(
            '/api/v2/orders/', data=json.dumps(self.more_fields), headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please ensure that you have only a Meal ids field')

    def test_empty_id_list(self):
        '''Check if meal ids are empty'''
        response = self.tester.post(
            '/api/v2/orders', data=json.dumps(self.empty_ids), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], "Please enter an id to add your meals to the menu")

    def test_wrong_id_input(self):
        '''Check if meal ids are not integers'''
        response = self.tester.post(
            '/api/v2/orders', data=json.dumps(self.wrong_input_data), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], "Please enter list id values for meals")

    def test_meal_ids_input_types(self):
        '''Check if meal ids should only be integers'''
        response = self.tester.post(
            '/api/v2/orders/', data=json.dumps(self.meal_ids_test), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], "List values should only be in numbers")

    # def test_id_that_is_not_in_menu(self):
    #     '''Check if meal id that doesnt exist'''
        # response = self.tester.post(
        #     '/api/v2/menu/', data=json.dumps(self.add_menu_data), headers=self.headers)
        # # self.assertEqual(response.status_code, 201)
        # data = json.loads(response.data)
        # print(data)

        # response = self.tester.post(
        #     '/api/v2/orders', data=json.dumps(self.wrong_data), headers=self.headers)
        # self.assertEqual(response.status_code, 404)
        # data = json.loads(response.data)
        # self.assertEqual(
        #     data['message'], "Please enter food that is in the menu")

    def test_meal_ids_neg_or_zero(self):
        '''Check if meal ids are negative or zero'''
        response = self.tester.post(
            '/api/v2/orders/', data=json.dumps(self.meal_ids_neg), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], "The id should not be 0 or a negative")

    def test_success_order(self):
        '''Check for successful order'''

        response = self.tester.post(
            '/api/v2/orders', data=json.dumps(self.add_order_data), headers=self.headers)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], "Your order was successfully created!")

    def test_order_available(self):
        '''Check if order exists'''
        response1 = self.tester.post(
            '/api/v2/orders', data=json.dumps(self.add_order_data), headers=self.headers)
        self.assertEqual(response1.status_code, 201)

        response = self.tester.post(
            '/api/v2/orders', data=json.dumps(self.add_order_data), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], "Sorry, the meal is already in your order")

    def test_wrong_fields_in_edit_order(self):
        '''Test if one enters no field, one field or more than two fields'''
        response = self.tester.post(
            '/api/v2/orders', data=json.dumps(self.add_order_data), headers=self.headers)
        self.assertEqual(response.status_code, 201)

        response = self.tester.put(
            '/api/v2/orders/1', data=json.dumps(self.no_field), headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please ensure that you have only a quantity field')

        response = self.tester.put(
            '/api/v2/orders/1', data=json.dumps(self.more_fields), headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Please ensure that you have only a quantity field')

    def test_order_doesnt_exist(self):
        '''Check if order doesnt exist'''
        response1 = self.tester.post(
            '/api/v2/orders', data=json.dumps(self.add_order_data), headers=self.headers)
        self.assertEqual(response1.status_code, 201)

        response = self.tester.put(
            '/api/v2/orders/7', data=json.dumps(self.qty), headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "The order was not found")

    def test_order_qty_empty(self):
        '''Check if qty is empty'''
        response1 = self.tester.post(
            '/api/v2/orders', data=json.dumps(self.add_order_data), headers=self.headers)
        self.assertEqual(response1.status_code, 201)

        response = self.tester.put(
            '/api/v2/orders/1', data=json.dumps(self.empty_qty), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], "Please enter the quantity you want to change to")

    def test_order_qty_wrong_input(self):
        '''Check if qty is not an integer'''
        response = self.tester.post(
            '/api/v2/orders', data=json.dumps(self.add_order_data), headers=self.headers)
        self.assertEqual(response.status_code, 201)

        response = self.tester.put(
            '/api/v2/orders/1', data=json.dumps(self.wrong_qty), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], "Please enter a number value for quantity")

    def test_order_qty_negative_or_zero(self):
        '''Check if qty is not an integer'''
        response1 = self.tester.post(
            '/api/v2/orders', data=json.dumps(self.add_order_data), headers=self.headers)
        self.assertEqual(response1.status_code, 201)

        response = self.tester.put(
            '/api/v2/orders/1', data=json.dumps(self.neg_qty), headers=self.headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], "Quantity should not be 0 or a negative")

    def test_order_success_modified(self):
        '''Check for a successful order modification'''
        response1 = self.tester.post(
            '/api/v2/orders', data=json.dumps(self.add_order_data), headers=self.headers)
        self.assertEqual(response1.status_code, 201)

        response = self.tester.put(
            '/api/v2/orders/1', data=json.dumps(self.qty), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], "Your order was successfully created!")

    def test_delete_when_order_unavailable(self):
        '''Check absence of order to be deleted'''
        response1 = self.tester.post(
            '/api/v2/orders', data=json.dumps(self.add_order_data), headers=self.headers)
        self.assertEqual(response1.status_code, 201)

        response = self.tester.delete('/api/v2/orders/9', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "The order was not found")

    def test_delete_order_success(self):
        '''Check for successful deletion of order'''
        response1 = self.tester.post(
            '/api/v2/orders', data=json.dumps(self.add_order_data), headers=self.headers)
        self.assertEqual(response1.status_code, 201)

        response = self.tester.delete('/api/v2/orders/1', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "The order has been removed")


if __name__ == "__main__":
    unittest.main()
