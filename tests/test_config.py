import sys  # fix import errors
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
            username="ian", email="ian@test.com", password=hashed_password, admin=True)
        self.new_user.save()

        # Create a new user 2
        hashed_password = generate_password_hash("#2345678", method='md5')
        self.new_user = User(
            username="ian5678", email="ian@test.com", password=hashed_password, admin=False)
        self.new_user.save()

        # Add new meal
        self.new_meal = Meals(meal_name="Rice", meal_price=200.00)
        self.new_meal.save()

        # Add new meal 2
        self.new_meal2 = Meals(meal_name="Pasta", meal_price=100.00)
        self.new_meal2.save()

        # Add new meal 3
        self.new_meal3 = Meals(meal_name="Beef", meal_price=150.00)
        self.new_meal3.save()

        self.tester = self.app.test_client()

        self.u_data = {
            "username": "ian",
            "password": "#2345"
        }

        response = self.tester.post(
            '/api/v2/auth/login', data=json.dumps(self.u_data), content_type='application/json')
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
