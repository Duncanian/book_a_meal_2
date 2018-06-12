from os import getenv
import datetime
import uuid
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource
import jwt
from models.models import User, Orders, Menu, db, Meals
from auth.token import token_required, admin_only


class AuthCreate(Resource):
    def post(self):
        post_data = request.get_json(force=True)

        if len(post_data) == 0 or len(post_data) == 1 or len(post_data) > 2:
            return {'message': 'Please ensure that you have only Username and Password fields'}, 404

        if not post_data['password'] or not post_data['username']:
            return {'message': 'Please enter all the details'}, 400

        if not isinstance(post_data['password'], str) or not isinstance(post_data['username'], str):
            return {'message': 'Please enter a string value for username and password'}, 400

        if len(post_data['username'].strip()) < len(post_data['username']):
            return {'message': 'Username should not have spaces!'}, 400

        if len(post_data['password']) < 5:
            return {'message': 'Password should be more than 5 characters'}, 400

        if len(post_data['password']) > 10:
            return {'message': 'Password should be less than 10 characters'}, 400

        user = User.query.filter_by(username=post_data['username']).first()

        if user:
            return {"message": "Sorry, username already taken!"}, 400

        hashed_password = generate_password_hash(
            post_data['password'], method='md5')
        new_user = User(
            username=post_data['username'], password=hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'New user created!'}, 201

    @admin_only
    def get(self, active_user):
        users = User.query.all()

        if not users:
            return {"message":"No users found"}, 404
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

        if len(post_data) == 0 or len(post_data) == 1 or len(post_data) > 2:
            return {'message': 'Please ensure that you have only Username and Password fields'}, 404

        if not post_data['password'] or not post_data['username']:
            return {'message': 'Please enter all the details'}, 400

        if not isinstance(post_data['password'], str) or not isinstance(post_data['username'], str):
            return {'message': 'Please enter a string value for username and password'}, 400

        user = User.query.filter_by(username=post_data['username']).first()

        if not user:
            return {'message': 'Please sign up then login'}, 404

        if check_password_hash(user.password, post_data['password']):
            token = jwt.encode({"user_id": user.id, "admin": user.admin, "exp": datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=30)}, getenv('SECRET_KEY'))
            return {"token": token.decode('UTF-8')}, 201
        return {"message": "wrong password, please try again"}, 401


class MenuOrders(Resource):
    """docstring for MenuOrders"""
    @token_required
    def get(self, active_user):
        #date = datetime.datetime.utcnow().date()
        menu = Menu.query.order_by(Menu.id.desc()).first()

        if not menu:
            return {"message":"No menu set up for today"}, 404
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
        date = datetime.datetime.utcnow().date()

        # deadline = datetime.time(15, 0, 0).hour
        # start = datetime.time(5, 0, 0).hour
        # current_time = datetime.datetime.utcnow().time().hour
        # if current_time > deadline or current_time < start:
        #     return {"message" : "Orders take place between 8:00 am to 3:00 pm only"}

        if len(post_data) == 0 or len(post_data) > 1:
            return {'message': 'Please ensure that you have only a Meal ids field'}, 404

        if not post_data['meal_ids']:
            return {"message": "Please enter an id to add your meals to the menu"}, 400

        if not isinstance(post_data['meal_ids'], list):
            return {'message': 'Please enter list id values for meals'}, 400

        for i in post_data['meal_ids']:
            if not isinstance(i, int):
                return {"message": "List values should only be in numbers"}, 400

            if i < 1:
                return {'message': 'The id should not be 0 or a negative'}, 400

        meal_ids = post_data['meal_ids']

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        user_det = jwt.decode(token, getenv('SECRET_KEY'))

        menu = Menu.query.order_by(Menu.id.desc()).first()
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

        incorrect = [
            meal_id for meal_id in meal_ids if meal_id not in meal_list]
        if len(incorrect) > 0:
            return {"message": 'Please enter food that is in the menu'}, 404

        for item in meal_list:
            orders = [order for order in output if order["id"] == item]
            one_order = orders[0]

            order_ava = Orders.query.filter_by(
                order_meal=one_order['meal_name'], order_date=str(date)).first()
            if order_ava:
                return {'message': 'Sorry, the meal is already in your order'}, 400

            new_order = Orders(order_meal=one_order['meal_name'],
                               order_price=one_order['meal_price'], qty=1, order_by=user_det['user_id'])
            db.session.add(new_order)
            db.session.commit()

        return {'message': 'Your order was successfully created!'}, 201

    @token_required
    def put(self, active_user, order_id):
        # change qty then multiply it to get the price

        post_data = request.get_json(force=True)
        deadline = datetime.time(15, 0, 0).hour
        current_time = datetime.datetime.utcnow().time().hour
        date = datetime.datetime.utcnow().date()
        order = Orders.query.filter_by(
            id=order_id, order_date=str(date)).first()

        if not order:
            return {"message": "The order was not found"}, 404

        if len(post_data) == 0 or len(post_data) > 1:
            return {'message': 'Please ensure that you have only a qty field'}, 404

        if current_time > deadline:
            return {"message" : "Your order has already expired, next time make a change before 3pm"}

        if not post_data['qty']:
            return {'message': 'Please enter the quantity you want to change to'}, 400

        if not isinstance(post_data['qty'], int):
            return {'message': 'Please enter a number value for quantity'}, 400

        if post_data['qty'] < 1:
            return {'message': 'Quantity should not be 0 or a negative'}, 400

        order.qty = post_data['qty']
        total = order.qty * order.order_price
        order.order_price = total
        db.session.commit()

        return {"status": "success", "data": 'Order modified!'}, 200

    @token_required
    def delete(self, active_user, order_id):
        date = datetime.datetime.utcnow().date()
        order = Orders.query.filter_by(
            id=order_id, order_date=str(date)).first()

        if not order:
            return {"message": "The order was not found"}, 404
        db.session.delete(order)
        db.session.commit()
        return {"message": "The order has been removed"}, 200
