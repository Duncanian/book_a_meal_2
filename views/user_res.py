from flask import jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from models.models import User, Orders, Menu, db, Meals
from flask_restful import Resource
import jwt

class AuthCreate(Resource):
    def post(self):
        if request.json:
            if request.json['password'] == '' or request.json['username'] == '':
                return jsonify({'message' : 'Please enter all the details'})

            if not isinstance(request.json['password'], str) or not isinstance(request.json['username'], str):
                return jsonify({'message' : 'Please enter a string value for username and password'})

            hashed_password = generate_password_hash(request.json['password'], method='md5')
            new_user = User(user_id = str(uuid.uuid4()), username = request.json['username'], 
                password = hashed_password, admin=False)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message' : 'New user created!'})

        # hashed_password = generate_password_hash(request.form.get('password'), method='md5')
        # new_user = User(user_id = str(uuid.uuid4()), username = request.form.get('username'), password = hashed_password, admin=False)
        # db.session.add(new_user)
        # db.session.commit()
        # return jsonify({'message' : 'New user created!'})

    def get(self):
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
        if request.json['password'] == '' or request.json['username'] == '':
            return jsonify({'message' : 'Please enter all the details'})

        if not isinstance(request.json['password'], str) or not isinstance(request.json['username'], str):
            return jsonify({'message' : 'Please enter a string value for username and password'})

        user = User.query.filter_by(username = request.json['username']).first()

        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        if check_password_hash(user.password, request.json['password']):
            token = jwt.encode({"user_id" : user.user_id, "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)}, "This is secret")
            return jsonify({"token" : token.decode('UTF-8')})
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

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
        meal = Meals.query.filter_by(meal_name=request.json['order_name']).first()

        if not meal:
            return jsonify({"message" : "The meal was not found"})

        order = Orders.query.filter_by(order_name=meal.meal_name).first()

        if not order:
            return jsonify({"message" : "The order was not found"})

        new_order = Orders(order_id = meal.meal_id, order_name = request.json['order_name'], order_price = request.json['order_price'],
            order_category = request.json['order_category'], order_day = request.json['order_day'], order_user = request.json['user'])
        #Add name from jwt
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message' : 'Your order has been placed!'})
        
    def put(self, order_id):
        order = Orders.query.filter_by(order_id=order_id).first()

        if not order:
            return jsonify({"message" : "The order was not found"})

        order.order_qty = request.json['order_qty']
        db.session.commit()

        return {"status": "success", "data": 'Order modified!'}, 200

    def delete(self, order_id):
        order = Orders.query.filter_by(order_id=order_id).first()

        if not order:
            return jsonify({"message" : "The order was not found"})
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message" : "The order has been removed"})