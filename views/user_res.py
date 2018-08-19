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

        if len(post_data) == 0 or len(post_data) == 1 or len(post_data) == 2 or len(post_data) > 3:
            return {'message': 'Please ensure that you have only Username, Email and Password fields'}, 400

        username = post_data['username']
        password = post_data['password']
        email = post_data['email']

        if not password or not username or not email:
            return {'message': 'Please enter all the details'}, 400

        if not isinstance(password, str) or not isinstance(username, str)or not isinstance(email, str):
            return {'message': 'Please enter a string value for username, email and password'}, 400

        if len(username.strip()) < len(username):
            return {'message': 'Username should not have spaces!'}, 400

        if len(password) < 5:
            return {'message': 'Password should be more than 5 characters'}, 400

        if len(password.strip()) < len(password):
            return {'message': 'Password should not have spaces!'}, 400

        user = User.query.filter_by(username=username).first()

        if user:
            return {"message": "Sorry, username already taken!"}, 400

        superuser = User.query.filter_by(username="admin").first()

        if not superuser:
            # Create a new user
            super_pass = generate_password_hash("admin", method='md5')
            self.admin = User(
                username="admin", password=super_pass, admin=True)
            self.admin.save()

        hashed_password = generate_password_hash(
            password, method='md5')
        new_user = User(
            username=username, email=email, password=hashed_password, admin=False)
        new_user.save()

        display_user = User.query.filter_by(username=username).first()

        user_data = {}
        user_data['id'] = display_user.id
        user_data['username'] = display_user.username
        user_data['email'] = display_user.email
        user_data['password'] = display_user.password

        return {'message': 'You have been successfully registered!', "data": user_data}, 201

    @admin_only
    def get(self, active_user):
        users = User.query.all()

        if not users:
            return {"message": "No users found"}, 204
            # Not yet tested this
        output = []
        for user in users:
            user_data = {}
            user_data['id'] = user.id
            user_data['username'] = user.username
            user_data['email'] = user.email
            user_data['password'] = user.password
            output.append(user_data)

        return {"status": "success", "data": output}, 200

    @admin_only
    def put(self, active_user, identity):
        user = User.query.filter_by(id=identity).first()

        if not user:
            return {"message": "No such user found"}, 404

        post_data = request.get_json(force=True)

        admin = post_data['admin']

        if not isinstance(admin, bool):
            return {'message': 'Please enter a boolean value for admin'}, 400

        user.admin = post_data['admin']
        db.session.commit()

        user_data = {}
        user_data['id'] = user.id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['admin'] = user.admin

        return {"status": "success", "message": "User successfully made an admin", "data": user_data}, 200


class AuthLogin(Resource):
    """docstring for AuthLogin"""

    def post(self):
        post_data = request.get_json(force=True)

        if len(post_data) == 0 or len(post_data) == 1 or len(post_data) > 2:
            return {'message': 'Please ensure that you have only Username and Password fields'}, 400

        username = post_data['username']
        password = post_data['password']

        if not password or not username:
            return {'message': 'Please enter all the details'}, 400

        if not isinstance(password, str) or not isinstance(username, str):
            return {'message': 'Please enter a string value for username and password'}, 400

        user = User.query.filter_by(username=username).first()

        if not user:
            return {'message': 'Please sign up then login'}, 404

        if check_password_hash(user.password, password):
            token = jwt.encode({"user_id": user.id, "admin": user.admin, "exp": datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=30)}, getenv('SECRET_KEY'))
            return {"token": token.decode('UTF-8')}, 201
        return {"message": "wrong password, please try again"}, 401


class Menus(Resource):
    """docstring for Get Menu"""
    @token_required
    def get(self, active_user):
        menu = Menu.query.order_by(Menu.id.desc()).first()
        if not menu:
            return {"message": "No menu set up for today"}, 404
        output = []
        for meal in menu.meals:
            menu_data = {}
            menu_data['menu_name'] = meal.meal_name
            menu_data['menu_price'] = meal.meal_price
            output.append(menu_data)

        return {"status": "success", "data": {"Id": menu.id, "Menu": menu.menu_name, "Meals": output}}, 200


class OrdersClass(Resource):
    """docstring for Orders"""

    @token_required
    def post(self, active_user):
        post_data = request.get_json(force=True)
        date = datetime.datetime.utcnow().date()

        deadline = datetime.time(23, 0, 0).hour
        start = datetime.time(5, 0, 0).hour
        current_time = datetime.datetime.utcnow().time().hour
        if current_time > deadline or current_time < start:
            return {"message": "Orders take place between 8:00 am to 11:00 pm only"}

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

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        user_det = jwt.decode(token, getenv('SECRET_KEY'))

        for item in meal_list:
            orders = [order for order in output if order["id"] == item]
            one_order = orders[0]

            order_ava = Orders.query.filter_by(
                order_meal=one_order['meal_name'], order_date=str(date)).first()
            if order_ava:
                return {'message': 'Sorry, the meal is already in your order'}, 400

            new_order = Orders(order_meal=one_order['meal_name'],
                               order_price=one_order['meal_price'], quantity=1, order_by=user_det['user_id'])
            new_order.save()

        orders = Orders.query.filter_by(order_date=str(
            date), order_by=user_det['user_id']).all()

        output_new = []
        for order in orders:
            order_data = {}
            order_data['id'] = order.id
            order_data['meal_name'] = order.order_meal
            order_data['meal_price'] = order.order_price
            order_data['order date'] = order.order_date
            order_data['order time'] = order.order_time
            order_data['quantity'] = order.quantity
            output_new.append(order_data)

        return {"status": "success", 'message': 'Your order was successfully created!', "data": {"My orders": output_new}}, 201

    @admin_only
    def get(self, active_user):
        orders = Orders.query.all()

        if not orders:
            return {"message": "Orders unavailable"}
        output = []
        for order in orders:
            order_data = {}
            order_data['id'] = order.id
            order_data['order_meal'] = order.order_meal
            order_data['order_price'] = order.order_price
            order_data['order_date'] = order.order_date
            order_data['order_time'] = order.order_time
            order_data['qty'] = order.qty
            order_data['user_id'] = order.order_by
            output.append(order_data)
        return {"status": "success", "data": output}, 200

    @token_required
    def put(self, active_user, order_id):
        # change qty then multiply it to get the price

        post_data = request.get_json(force=True)

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        user_det = jwt.decode(token, getenv('SECRET_KEY'))

        deadline = datetime.time(23, 0, 0).hour
        current_time = datetime.datetime.utcnow().time().hour
        date = datetime.datetime.utcnow().date()
        order = Orders.query.filter_by(
            id=order_id, order_date=str(date), order_by=user_det['user_id']).first()

        if not order:
            return {"message": "The order was not found"}, 404

        if len(post_data) == 0 or len(post_data) > 1:
            return {'message': 'Please ensure that you have only a quantity field'}, 404

        if current_time > deadline:
            return {"message": "Your order has already expired, next time make a change before 11pm"}

        if not post_data['quantity']:
            return {'message': 'Please enter the quantity you want to change to'}, 400

        if not isinstance(post_data['quantity'], int):
            return {'message': 'Please enter a number value for quantity'}, 400

        if post_data['quantity'] < 1:
            return {'message': 'Quantity should not be 0 or a negative'}, 400

        order.qty = post_data['quantity']
        total = order.qty * order.order_price
        order.order_price = total
        db.session.commit()

        order_data = {}
        order_data['id'] = order.id
        order_data['meal_name'] = order.order_meal
        order_data['meal_price'] = order.order_price
        order_data['order date'] = order.order_date
        order_data['order time'] = order.order_time
        order_data['quantity'] = order.quantity

        return {"status": "success", "message": "Your order was successfully created!", "data": order_data}, 200

    @token_required
    def delete(self, active_user, order_id):
        date = datetime.datetime.utcnow().date()

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        user_det = jwt.decode(token, getenv('SECRET_KEY'))

        order = Orders.query.filter_by(
            id=order_id, order_date=str(date), order_by=user_det['user_id']).first()

        if not order:
            return {"message": "The order was not found"}, 404
        order.delete()
        return {"status": "success", "message": "The order has been removed"}, 200
