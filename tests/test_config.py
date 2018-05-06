import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from unittest import TestCase
import uuid
from base import create_app
from config import config
from models.models import User, Orders, Menu, db, Meals
from werkzeug.security import generate_password_hash



class GroundTests(TestCase):
    '''The Founding tests for the DB'''

    def setUp(self):
        '''The first step for it's run'''
        self.app = create_app(config['testing'])
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

        # Create a new user
        hashed_password = generate_password_hash("#2345", method='md5')
        self.new_user = User(
            username="ian", password=hashed_password, admin=True)
        db.session.add(self.new_user)
        db.session.commit()

        # Add new meal
        self.new_meal = Meals(meal_name="Rice", meal_price=200)
        db.session.add(self.new_meal)
        db.session.commit()

        # Add new meal 2
        self.new_meal2 = Meals(meal_name="Pasta", meal_price=100)
        db.session.add(self.new_meal2)
        db.session.commit()

        # Add new meal 3
        self.new_meal3 = Meals(meal_name="Beef", meal_price=150)
        db.session.add(self.new_meal3)
        db.session.commit()

        self.tester = self.app.test_client()

        self.u_data = {
            "username": "ian",
            "password": "#2345"
        }

        response = self.tester.post(
            '/api/v2/auth/login', data=json.dumps(self.u_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.token = data['token']

        self.headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
