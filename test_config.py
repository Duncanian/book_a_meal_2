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

        #Create a new user
        hashed_password = generate_password_hash("#2345", method='md5')
        self.new_user = User(user_id = str(uuid.uuid4()), username="ian", password=hashed_password, admin=True)
        db.session.add(self.new_user)
        db.session.commit()

        #Add new meal
        self.new_meal = Meals(meal_id = str(uuid.uuid4()), meal_name = "Rice with beef", meal_price = 200,
            meal_category = "lunch", meal_day = 'monday')
        db.session.add(self.new_meal)
        db.session.commit()

        #Add new meal 2
        self.new_meal = Meals(meal_id = str(uuid.uuid4()), meal_name = "Pasta with beef", meal_price = 300,
            meal_category = "lunch", meal_day = 'tuesday')
        db.session.add(self.new_meal)
        db.session.commit()

        #Add meal to menu
        self.meal = Meals.query.filter_by(meal_name='Rice with beef').first()
        self.new_menu = Menu(menu_id = self.meal.meal_id, menu_name = "Rice with beef", menu_price = 200,
            menu_category = "lunch", menu_day = 'monday')
        db.session.add(self.new_menu)
        db.session.commit()

        #Add meal in menu to order
        self.menu = Menu.query.filter_by(menu_name='Rice with beef').first()
        self.new_order = Orders(order_id = self.menu.menu_id, order_name = 'Rice with beef', order_price = 200,
            order_category = 'lunch', order_day = 'monday', order_qty=1, order_user = 'ian')
        db.session.add(self.new_order)
        db.session.commit()

        #Add new meal 2
        self.new_meal2 = Meals(meal_id = str(uuid.uuid4()), meal_name = "Milk with Bread", meal_price = 70,
            meal_category = "breakfast", meal_day = 'tuesday')
        db.session.add(self.new_meal2)
        db.session.commit()

        #Add meal to menu 2
        self.meal2 = Meals.query.filter_by(meal_name='Milk with Bread').first()
        self.new_menu2 = Menu(menu_id = self.meal2.meal_id, menu_name = "Milk with Bread", menu_price = 70,
            menu_category = "breakfast", menu_day = 'tuesday')
        db.session.add(self.new_menu2)
        db.session.commit()

        self.tester = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

