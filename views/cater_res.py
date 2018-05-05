import uuid
from os import getenv
import datetime
import jwt
from flask import request
from flask_restful import Resource
from models.models import Meals, Orders, Menu, db
from auth.token import token_required, admin_only


class MealMan(Resource):
	"""docstring for Meal_man"""
	@admin_only
	def post(self, active_user):
		post_data = request.get_json(force=True)
		meal = Meals.query.filter_by(meal_name=post_data['meal_name']).first()

		if not post_data['meal_name'] or not post_data['meal_price']:
			return {'message' : 'Please enter all the details'}, 200

		if not isinstance(post_data['meal_price'], int):
			return {'message' : 'Price should be a number'}, 200

		if not isinstance(post_data['meal_name'], str):
			return {'message' : 'Please enter a string value for meal'}, 200

		if len(post_data['meal_name'].strip()) < len(post_data['meal_name']):
			return {'message' : 'Meal name should not have spaces!'}, 200

		if meal:
			return {"message" : "The meal already exists"}, 200

		new_meal = Meals(meal_name = post_data['meal_name'], meal_price = post_data['meal_price'])
		db.session.add(new_meal)
		db.session.commit()
		return {'message' : 'New meal added!'}, 200

	@admin_only
	def get(self, active_user):
		meals = Meals.query.all()
		output = []
		for meal in meals:
			meal_data = {}
			meal_data['meal_id'] = meal.id
			meal_data['meal_name'] = meal.meal_name
			meal_data['meal_price'] = meal.meal_price
			output.append(meal_data)

		return {"status": "success", "data": output}, 200

	@admin_only
	def put(self, active_user, meal_id):
		post_data = request.get_json(force=True)
		meal = Meals.query.filter_by(id=meal_id).first()

		if not post_data['meal_name'] or not post_data['meal_price']:
			return {'message' : 'Please enter all the details'}, 200

		if not isinstance(post_data['meal_name'], str):
			return {'message' : 'Please enter a string value for meal'}, 200

		if not isinstance(post_data['meal_price'], int):
			return {'message' : 'Please enter a number value for price'}, 200

		if len(post_data['meal_name'].strip()) < len(post_data['meal_name']):
			return {'message' : 'Meal name should not have spaces!'}, 200

		if not meal:
			return {"message" : "The meal was not found"}, 200

		meal.meal_name = post_data['meal_name']
		meal.meal_price = post_data['meal_price']
		db.session.commit()

		return {"status": "success", "data": 'Meal modified!'}, 200

	@admin_only
	def delete(self, active_user, meal_id):
		meal = Meals.query.filter_by(id=meal_id).first()

		if not meal:
			return {"message" : "The meal was not found"}, 200
		db.session.delete(meal)
		db.session.commit()
		return {"message" : "The meal has been deleted"}, 200

class Menus(Resource):
	"""docstring for Menu"""
	@admin_only
	def post(self, active_user):
		post_data = request.get_json(force=True)

		if not post_data['meal_ids']:
			return {"message":"Please enter an id to add your meals to the menu"}, 200

		if not isinstance(post_data['meal_ids'], list):
			return {'message' : 'Please enter list id values for meals'}, 200

		for i in post_data['meal_ids']:
			if not isinstance(i, int):
				return {"message":"List values should only be in numbers"}, 200

		if not post_data['menu_name']:
			return {'message' : 'Please enter the Menu name'}, 200

		if not isinstance(post_data['menu_name'], str):
			return {'message' : 'Please enter a string value for Menu name'}, 200

		if len(post_data['menu_name'].strip()) < len(post_data['menu_name']):
			return {'message' : 'Menu name should not have spaces!'}, 200

		meal_ids = post_data['meal_ids']
		menu_meals = []
		for i in meal_ids:
			meal = Meals.query.filter_by(id=i).first()
			if not meal:
				return {"message" : "The meal was not found"}, 200
			menu_meals.append(meal)

		menu = Menu.query.filter_by(menu_name=post_data['menu_name']).first()
		if menu:
			return {'message':"Menu already available!"}, 200

		new_menu = Menu(menu_name = post_data['menu_name'])
		db.session.add(new_menu)
		db.session.commit()
		new_menu = Menu.query.filter_by(id=new_menu.id).first()
		new_menu.meals.extend(menu_meals)
		db.session.add(new_menu)
		db.session.commit()
		return {'message' : 'New meal added to the menu!'}, 200

class OrdersAll(Resource):
	"""docstring for Orders"""
	@admin_only
	def get(self, active_user):
		if 'Authorization' in request.headers:
			token = request.headers['Authorization']

		user_det = jwt.decode(token, getenv('SECRET_KEY'))

		orders = Orders.query.filter_by(order_by=user_det['user_id']).all()
		output = []
		for order in orders:
			order_data = {}
			order_data['id'] = order.id
			order_data['order_meal'] = order.order_meal
			order_data['order_price'] = order.order_price
			order_data['time_ordered'] = str(order.time_ordered)
			order_data['qty'] = order.qty
			output.append(order_data)
		return {"status": "success", "data": output}, 200
