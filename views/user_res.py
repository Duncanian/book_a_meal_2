from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from models.models import User, Orders, Menu, db, Meals
from flask_restful import Resource
import jwt
from os import getenv
import datetime
from auth.token import token_required, admin_only

class AuthCreate(Resource):
    def post(self):
        post_data = request.get_json(force=True)

        if not post_data['password'] or not post_data['username']:
            return {'message' : 'Please enter all the details'}, 200

        if not isinstance(post_data['password'], str) or not isinstance(post_data['username'], str):
            return {'message' : 'Please enter a string value for username and password'}, 200

        if len(post_data['username'].strip()) < len(post_data['username']):
            return {'message' : 'Username should not have spaces!'}, 200

        if len(post_data['password']) < 5:
            return {'message' : 'Password should be more than 5 characters'}, 200

        if len(post_data['password']) > 10:
            return {'message' : 'Password should be less than 10 characters'}, 200

        user = User.query.filter_by(username = post_data['username']).first()

        if user:
            return {"message":"Sorry, username already taken!"}

        hashed_password = generate_password_hash(post_data['password'], method='md5')
        new_user = User(username = post_data['username'], password = hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit()
        return {'message' : 'New user created!'}, 200

    @admin_only
    def get(self, active_user):
    	users = User.query.all()
    	output = []
    	for user in users:
    		user_data = {}
    		user_data['id'] = user.id
    		user_data['username'] = user.username
    		user_data['password'] = user.password
    		output.append(user_data)

    	return {"status": "success", "data": output}, 200

class AuthLogin(Resource):
    """docstring for AuthLogin"""
    def post(self):
        post_data = request.get_json(force=True)

        if not post_data['password'] or not post_data['username']:
            return {'message' : 'Please enter all the details'}, 200

        if not isinstance(post_data['password'], str) or not isinstance(post_data['username'], str):
            return {'message' : 'Please enter a string value for username and password'}, 200

        user = User.query.filter_by(username = post_data['username']).first()

        if not user:
            return {'message' : 'Please sign up then login'}, 200

        if check_password_hash(user.password, post_data['password']):
            token = jwt.encode({"user_id" : user.id, "admin":user.admin, "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)}, getenv('SECRET_KEY'))
            return {"token" : token.decode('UTF-8')}, 200
        return {"message":"wrong password, please try again"}, 200
        

class MenuOrders(Resource):
    """docstring for MenuOrders"""
    @token_required
    def get(self, active_user):
        #date = datetime.datetime.utcnow().date()
        menu = Menu.query.filter_by(id=1).first()
        output = []
        for meal in menu.meals:
            menu_data = {}
            menu_data['menu_name'] = meal.meal_name
            menu_data['menu_price'] = meal.meal_price
            output.append(menu_data)

        return {"status": "success", "data": output}, 200

    @token_required
    def post(self, active_user):
        post_data = request.get_json(force=True)

        if not post_data['meal_ids']:
            return {"message":"Please enter an id to add your meals to the menu"}, 200

        if not isinstance(post_data['meal_ids'], list):
            return {'message' : 'Please enter list id values for meals'}, 200

        for i in post_data['meal_ids']:
            if not isinstance(i, int):
                return {"message":"List values should only be in numbers"}, 200

        meal_ids = post_data['meal_ids']

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        user_det = jwt.decode(token, getenv('SECRET_KEY'))

        menu = Menu.query.filter_by(id=1).first()
        meal_list = []
        output = []
        for meal in menu.meals:
            yes = [x for x in meal_ids if x == meal.id]
            meal_list.append(yes[0])

            menu_data = {}
            menu_data['id'] = meal.id
            menu_data['meal_name'] = meal.meal_name
            menu_data['meal_price'] = meal.meal_price
            output.append(menu_data)

        incorrect = [meal_id for meal_id in meal_ids if meal_id not in meal_list]
        if len(incorrect) > 0:
            return {"message" : 'Please enter food that is in the menu'}, 200

        for item in meal_list:
            orders = [order for order in output if order["id"] == item]
            one_order = orders[0]

            order_ava = Orders.query.filter_by(order_meal=one_order['meal_name']).first()
            if order_ava:
                return {'message' : 'Sorry, the meal is already in your order'}, 200

            new_order = Orders(order_meal = one_order['meal_name'], 
                               order_price = one_order['meal_price'], qty=1, order_by=user_det['user_id'])
            db.session.add(new_order)
            db.session.commit()
        
        return {'message' : 'Your order was successfully created!'}, 200

    @token_required
    def put(self, active_user, order_id):
        #change qty then multiply it to get the price

        post_data = request.get_json(force=True)
        order = Orders.query.filter_by(id=order_id).first()

        if not order:
            return {"message" : "The order was not found"}, 200

        if not post_data['qty']:
            return {'message' : 'Please enter the quantity you want to change to'}, 200

        if not isinstance(post_data['qty'], int):
            return {'message' : 'Please enter a number value for quantity'}, 200

        order.qty = post_data['qty']
        total = order.qty * order.order_price
        order.order_price = total
        db.session.commit()

        return {"status": "success", "data": 'Order modified!'}, 200

    @token_required
    def delete(self, active_user, order_id):
        order = Orders.query.filter_by(id=order_id).first()

        if not order:
            return {"message" : "The order was not found"}, 200
        db.session.delete(order)
        db.session.commit()
        return {"message" : "The order has been removed"}, 200