import json
import unittest
import uuid
from test_config import GroundTests
from models.models import Orders

class TestMeals(GroundTests):
    def setUp(self):
        GroundTests.setUp(self)

        #Add meal to menu
        self.add_menu_data = {
            "menu_name": "Pasta with beef",
            "menu_price": 300,
            "menu_category"   : "lunch",
            "menu_day": "tuesday"
        }

        #Add none existing meal to menu
        self.add_bad_data = {
            "menu_name": "Chapatti with Beef",
            "menu_price": 250,
            "menu_category"   : "dinner",
            "menu_day": "monday"
        }

        # Add non-existing data to order
        self.none_order = {
            "order_name": "Chapatti with Beef",
            "order_price": 250,
            "order_category"   : "dinner",
            "order_day": "monday",
            "order_qty" : 1,
            "order_user" : "ian"
        }

        #Add existing order in orders to order
        self.existing_order = {
            "order_name": "Rice with beef",
            "order_price": 200,
            "order_category"   : "lunch",
            "order_day": "monday",
            "order_qty" : 1,
            "order_user" : "ian"
        }

        #Add new order to orders
        self.newest_order = {
            "order_name": "Milk with Bread",
            "order_price": 70,
            "order_category"   : "breakfast",
            "order_day": "tuesday",
            "order_qty" : 1,
            "order_user" : "ian"
        }

        self.avail_order = Orders.query.filter_by(order_name="Rice with beef").first()

        self.qty = {
            "order_qty" : 3
        }

        # response = self.client.post(self.login_url, data=self.data)
        # self.token = json.loads(response.data)["token"]
        # self.headers = {
        #     'Authorization': 'Bearer ' + self.token,
        #     'Content-Type': 'application/json',
        #     'Accept': 'application/json',
        # }
    def tearDown(self):
        GroundTests.tearDown(self)

    def test_meal_existence(self):
        '''Check if meal exists'''
        response = self.tester.post('/api/v1/menu/', data=json.dumps(self.add_bad_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "The meal was not found")

    # def test_meal_added_to_menu(self):
    #     '''Add meal successfully to menu'''
    #     response = self.tester.post('/api/v1/menu/', data=json.dumps(self.add_menu_data), content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data)
    #     self.assertEqual(data['message'], 'New meal added to the menu!')

    def test_get_menu(self):
        '''Get the menu for the day'''
        response = self.tester.get('/api/v1/menu/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data['data'], list, msg='Incorrect output type')

    def test_meal_in_menu(self):
        '''Check if meal is in menu before order'''
        response = self.tester.post('/api/v1/orders', data=json.dumps(self.none_order), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "The meal was not found in menu")

    def test_meal_already_ordered(self):
        '''Check if order exists'''
        response = self.tester.post('/api/v1/orders', data=json.dumps(self.existing_order), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "The order exist!")

    def test_meal_order_success(self):
        '''Add order successfully'''
        response = self.tester.post('/api/v1/orders', data=json.dumps(self.newest_order), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Your order has been placed!')

    def test_none_existing_order_before_edit(self):
        '''Check if meal exists in db'''
        response = self.tester.put('/api/v1/orders/24567876543234567876543', data=json.dumps(self.qty), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "The order was not found")

    def test_edit_success(self):
        '''Edit existing meal'''
        response = self.tester.put('/api/v1/orders/'+str(self.avail_order.order_id), data=json.dumps(self.qty), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['data'], 'Order modified!')

    def test_order_present_before_deleting(self):
        '''Check presence of order to be deleted'''
        response = self.tester.delete('/api/v1/orders/24567876543234567876543', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "The order was not found")

    def test_order_delete_success(self):
        '''Check for successful deletion of order'''
        response = self.tester.delete('/api/v1/orders/'+str(self.avail_order.order_id), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "The order has been removed")

if __name__ == "__main__":
    unittest.main()
