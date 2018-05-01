from flask import jsonify, request, make_response
import uuid
from models.models import Meals, Orders, Menu, db
from flask_restful import Resource

class Meal_man(Resource):
	"""docstring for Meal_man"""
	def post(self):
		if request.json['meal_name'] == '' or request.json['meal_price'] == '':
			return jsonify({'message' : 'Please enter all the details'})

		if not isinstance(request.json['meal_name'], str):
			return jsonify({'message' : 'Please enter a string value for meal'})

		new_meal = Meals(meal_id = str(uuid.uuid4()), meal_name = request.json['meal_name'], meal_price = request.json['meal_price'],
			meal_category = request.json['meal_category'], meal_day = request.json['meal_day'])
		db.session.add(new_meal)
		db.session.commit()
		return jsonify({'message' : 'New meal added!'})

	def get(self):
		meals = Meals.query.all()
		output = []
		for meal in meals:
			meal_data = {}
			meal_data['meal_id'] = meal.meal_id
			meal_data['meal_name'] = meal.meal_name
			meal_data['meal_price'] = meal.meal_price
			meal_data['meal_category'] = meal.meal_category
			meal_data['meal_day'] = meal.meal_day
			output.append(user_data)

		return {"status": "success", "data": output}, 200

	def put(self, meal_id):
		meal = Meals.query.filter_by(meal_id=meal_id).first()

		if not meal:
			return jsonify({"message" : "The meal was not found"})

		if request.json['meal_name'] == '' or request.json['meal_price'] == '':
			return jsonify({'message' : 'Please enter all the details'})

		if not isinstance(request.json['meal_name'], str):
			return jsonify({'message' : 'Please enter a string value for meal'})

		meal.meal_name = request.json['meal_name']
		meal.meal_price = request.json['meal_price']
		meal.meal_category = request.json['meal_category']
		meal.meal_day = request.json['meal_day']
		db.session.commit()

		return {"status": "success", "data": 'Meal modified!'}, 200

	def delete(self, meal_id):
		meal = Meals.query.filter_by(meal_id=meal_id).first()

		if not meal:
			return jsonify({"message" : "The meal was not found"})
		db.session.delete(meal)
		db.session.commit()
		return jsonify({"message" : "The meal has been deleted"})

class Menu(Resource):
	"""docstring for Menu"""
	def post(self):
		meal = Meals.query.filter_by(meal_name=request.json['meal_name']).first()

		if not meal:
			return jsonify({"message" : "The meal was not found"})

		new_menu = Menu(menu_id = meal.meal_id, menu_name = request.json['meal_name'], menu_price = request.json['meal_price'],
			menu_category = request.json['meal_category'], menu_day = request.json['meal_day'])
		db.session.add(new_menu)
		db.session.commit()
		return jsonify({'message' : 'New meal added to the menu!'})

class Orders_all(Resource):
	"""docstring for Orders"""
	def get(self):
		orders = Orders.query.all()
		output = []
		for order in orders:
			order_data = {}
			order_data['order_id'] = order.order_id
			order_data['order_name'] = order.order_name
			order_data['order_price'] = order.order_price
			order_data['order_category'] = order.order_category
			order_data['order_day'] = order.order_day
			order_data['order_qty'] = order.order_qty
			order_data['order_user'] = order.order_user
			output.append(order_data)
		return {"status": "success", "data": output}, 200
