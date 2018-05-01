from unittest import TestCase
import uuid
from base import create_app
from config import config
from models.models import User, Orders, Menu, db, Meals

class BaseTestCase():
    def setUp(self):
    	self.app = create_app(config['testing'])
    	self.app_context = self.app.app_context()
    	self.app_context.push()
    	db.drop_all()
    	db.create_all()

    	self.new_user = User(user_id = str(uuid.uuid4()), username="ian", password="#2345", admin=True)
    	db.session.add(self.new_user)
    	db.session.commit()

    	self.registerdata = {
            "user_id" : str(uuid.uuid4()),
            "username": "three",
            "password": "#2345"
        }
    # def tearDown(self):
    #     database.session.remove()
    #     database.drop_all()
    #     self.app_context.pop()
BaseTestCase().setUp()