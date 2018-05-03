from flask import jsonify, request, make_response
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

        if post_data['password'] == '' or post_data['username'] == '':
            return jsonify({'message' : 'Please enter all the details'})

        if not isinstance(post_data['password'], str) or not isinstance(post_data['username'], str):
            return jsonify({'message' : 'Please enter a string value for username and password'})

        hashed_password = generate_password_hash(post_data['password'], method='md5')
        new_user = User(user_id = str(uuid.uuid4()), username = post_data['username'], 
            password = hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message' : 'New user created!'})

        # hashed_password = generate_password_hash(request.form.get('password'), method='md5')
        # new_user = User(user_id = int(uuid.uuid4()), username = request.form.get('username'), password = hashed_password, admin=False)
        # db.session.add(new_user)
        # db.session.commit()
        # return jsonify({'message' : 'New user created!'})

    @admin_only
    def get(self, active_user):
    	users = User.query.all()
    	output = []
    	for user in users:
    		user_data = {}
    		user_data['user_id'] = user.user_id
    		user_data['username'] = user.username
    		user_data['password'] = user.password
    		output.append(user_data)

    	return {"status": "success", "data": output}, 200

class AuthLogin(Resource):
    """docstring for AuthLogin"""
    def post(self):
        post_data = request.get_json(force=True)

        if post_data['password'] == '' or post_data['username'] == '':
            return jsonify({'message' : 'Please enter all the details'})

        if not isinstance(post_data['password'], str) or not isinstance(post_data['username'], str):
            return jsonify({'message' : 'Please enter a string value for username and password'})

        user = User.query.filter_by(username = post_data['username']).first()

        if not user:
            return jsonify({'message' : 'Please sign up then login'})

        if check_password_hash(user.password, post_data['password']):
            token = jwt.encode({"user_id" : user.user_id, "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)}, getenv('SECRET_KEY'), algorithm='HS256')
            return jsonify({"token" : token.decode('UTF-8')})
        return {"message":"wrong password, please try again"}
        

class MenuOrders(Resource):
    """docstring for MenuOrders"""
    def get(self):
        menu = Menu.query.all()
        output = []
        for meal in menu:
            menu_data = {}
            menu_data['menu_name'] = meal.menu_name
            menu_data['menu_price'] = meal.menu_price
            menu_data['menu_category'] = meal.menu_category
            menu_data['menu_day'] = meal.menu_day
            output.append(menu_data)

        return {"status": "success", "data": output}, 200

    def post(self):
        post_data = request.get_json(force=True)
        meal = Menu.query.filter_by(menu_name=post_data['order_name']).first()

        if not meal:
            return jsonify({"message" : "The meal was not found in menu"})

        order = Orders.query.filter_by(order_name=meal.menu_name).first()

        if order:
            return jsonify({"message" : "The order exist!"})

        new_order = Orders(order_id = meal.menu_id, order_name = post_data['order_name'], order_price = post_data['order_price'],
            order_category = post_data['order_category'], order_day = post_data['order_day'], order_qty=1, order_user = post_data['order_user'])
        #Add name from jwt
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message' : 'Your order has been placed!'})
        
    def put(self, order_id):
        post_data = request.get_json(force=True)
        order = Orders.query.filter_by(order_id=order_id).first()

        if not order:
            return jsonify({"message" : "The order was not found"})

        order.order_qty = post_data['order_qty']
        db.session.commit()

        return {"status": "success", "data": 'Order modified!'}, 200

    def delete(self, order_id):
        order = Orders.query.filter_by(order_id=order_id).first()

        if not order:
            return jsonify({"message" : "The order was not found"})
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message" : "The order has been removed"})