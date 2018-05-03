import json
import unittest
import uuid
from test_config import GroundTests
from models.models import Meals

class TestMeals(GroundTests):
    def setUp(self):
        GroundTests.setUp(self)
        #Add meal
        self.add_meal_data = {
            "meal_id" : str(uuid.uuid4()),
            "meal_name": "Chapatti with Beef",
            "meal_price": 250,
            "meal_category"   : "dinner",
            "meal_day": "monday"
        }

        #A missing detail in register details
        self.add_miss_data = {
            "meal_id" : str(uuid.uuid4()),
            "meal_name": "",
            "meal_price": 250,
            "meal_category"   : "dinner",
            "meal_day": "monday"
        }

        #Wrong data type for meal_name
        self.meal_name_typo = {
            "meal_id" : str(uuid.uuid4()),
            "meal_name": 123,
            "meal_price": 250,
            "meal_category"   : "dinner",
            "meal_day": "monday"
        }

        #Wrong data type for meal_price
        self.meal_price_typo = {
            "meal_id" : str(uuid.uuid4()),
            "meal_name": "Chapatti with Beef",
            "meal_price": '250',
            "meal_category"   : "dinner",
            "meal_day": "monday"
        }

        #Modify meal
        self.modify_meal = {
            "meal_name": "kuku with rice",
            "meal_price": 280,
            "meal_category" : "lunch",
            "meal_day": "tuesday"
        }

        #Modify meal with empty inputs
        self.mod_emp_meal = {
            "meal_name": "",
            "meal_price": 280,
            "meal_category"   : "lunch",
            "meal_day": "tuesday"
        }

        #Modify meal with meal name not string
        self.mod_int_meal = {
            "meal_name": 1234567,
            "meal_price": 280,
            "meal_category"   : "lunch",
            "meal_day": "tuesday"
        }


        self.meal = Meals.query.filter_by(meal_name='Rice with beef').first()

        self.test_meal = Meals.query.filter_by(meal_id=self.meal.meal_id).first()

        # response = self.client.post(self.login_url, data=self.data)
        # self.token = json.loads(response.data)["token"]
        # self.headers = {
        #     'Authorization': 'Bearer ' + self.token,
        #     'Content-Type': 'application/json',
        #     'Accept': 'application/json',
        # }
    def tearDown(self):
        GroundTests.tearDown(self)

    def test_add_meal(self):
        '''Add meal successfully to db'''
        response = self.tester.post('/api/v1/meals/', data=json.dumps(self.add_meal_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'New meal added!')

    def test_missing_data_in_input(self):
        '''Check if empty data will go through'''
        response = self.tester.post('/api/v1/meals/', data=json.dumps(self.add_miss_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Please enter all the details')

    def test_type_of_meal_name(self):
        '''Check if meal to be added is a string'''
        response = self.tester.post('/api/v1/meals/', data=json.dumps(self.meal_name_typo), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Please enter a string value for meal')

    def test_type_of_meal_price(self):
        '''Check if meal price is an integer'''
        response = self.tester.post('/api/v1/meals/', data=json.dumps(self.meal_price_typo), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Price should be a number')

    def test_get_meals(self):
        '''Check if meal data is available'''
        response = self.tester.get('/api/v1/meals/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data['data'], list, msg='Incorrect output type')

    def test_meal_exists(self):
        '''Check if meal exists in db'''
        response = self.tester.put('/api/v1/meals/hvgvg', data=json.dumps(self.modify_meal), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "The meal was not found")

    def test_empty_inputs_in_put(self):
        '''Check if some inputs are empty'''
        response = self.tester.put('/api/v1/meals/'+self.test_meal.meal_id, data=json.dumps(self.mod_emp_meal), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Please enter all the details')

    def test_meal_name_not_string(self):
        '''Check if meal name is not a string'''
        response = self.tester.put('/api/v1/meals/'+self.test_meal.meal_id, data=json.dumps(self.mod_int_meal), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Please enter a string value for meal')

    def test_modified_success(self):
        '''Check for successful meal modification'''
        response = self.tester.put('/api/v1/meals/'+self.test_meal.meal_id, data=json.dumps(self.modify_meal), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['data'], 'Meal modified!')

    def test_delete_when_meal_unavailable(self):
        '''Check presenec of meal to be deleted'''
        response = self.tester.delete('/api/v1/meals/iugyftg', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "The meal was not found")

    def test_delete_success(self):
        '''Check for successful deletion of meal'''
        response = self.tester.delete('/api/v1/meals/'+self.test_meal.meal_id, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "The meal has been deleted")

if __name__ == "__main__":
    unittest.main()