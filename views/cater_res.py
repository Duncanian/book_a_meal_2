import uuid
from os import getenv
import datetime
import jwt
from flask import request, jsonify
from flask_restful import Resource
from models.models import Meals, Orders, Menu, db
from auth.token import token_required, admin_only


class MealMan(Resource):
    """docstring for Meal_man"""
    @admin_only
    def post(self, active_user):
        post_data = request.get_json(force=True)

        if len(post_data) == 0 or len(post_data) == 1 or len(post_data) > 2:
            return {'message': 'Please ensure that you have only Meal Name and Meal Price fields'}, 400

        meal_name = post_data['meal_name']
        meal_price = post_data['meal_price']

        meal = Meals.query.filter_by(meal_name=meal_name).first()

        if not meal_name or not meal_price:
            return {'message': 'Please enter all the details'}, 400

        if not isinstance(meal_price, float):
            return {'message': 'Price should be a float'}, 400

        if not isinstance(meal_name, str):
            return {'message': 'Please enter a string value for meal'}, 400

        if meal_price < 1:
            return {'message': 'Meal Price should not be 0 or a negative'}, 400

        if meal:
            return {"message": "The meal already exists"}, 400

        new_meal = Meals(
            meal_name=meal_name, meal_price=round(meal_price, 2))
        new_meal.save()

        new_meal = Meals.query.filter_by(meal_name=meal_name).first()

        meal_data = {}
        meal_data['meal_id'] = new_meal.id
        meal_data['meal_name'] = new_meal.meal_name
        meal_data['meal_price'] = new_meal.meal_price

        return {"status": "success", 'message': 'New meal added!', "data": meal_data}, 201

    @admin_only
    def get(self, active_user):
        meals = Meals.query.all()

        if not meals:
            return {"message": "No meal available"}, 404
            # status code
            # Write test for this
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

        if not meal:
            return {"message": "The meal was not found"}, 404

        if len(post_data) == 0 or len(post_data) == 1 or len(post_data) > 2:
            return {'message': 'Please ensure that you have only Meal Name and Meal Price fields'}, 400

        meal_name = post_data['meal_name']
        meal_price = post_data['meal_price']

        if not meal_name or not meal_price:
            return {'message': 'Please enter all the details'}, 400

        if not isinstance(meal_name, str):
            return {'message': 'Please enter a string value for meal'}, 400

        if not isinstance(meal_price, float):
            return {'message': 'Please enter a float value for price'}, 400

        if post_data['meal_price'] < 1:
            return {'message': 'Meal Price should not be 0 or a negative'}, 400

        meal.meal_name = meal_name
        meal.meal_price = round(meal_price, 2)
        db.session.commit()

        meal_data = {}
        meal_data['meal_id'] = meal.id
        meal_data['meal_name'] = meal.meal_name
        meal_data['meal_price'] = meal.meal_price

        return {"status": "success", "message": 'Meal modified!', "data": meal_data}, 200

    @admin_only
    def delete(self, active_user, meal_id):
        meal = Meals.query.filter_by(id=meal_id).first()

        if not meal:
            return {"message": "The meal was not found"}, 404
        meal.delete()
        return {"message": "The meal has been deleted"}, 200


class Setmenu(Resource):
    """docstring for Menu"""
    @admin_only
    def post(self, active_user):
        post_data = request.get_json(force=True)

        if len(post_data) == 0 or len(post_data) == 1 or len(post_data) > 2:
            return {'message': 'Please ensure that you have Meal ids and Menu Name fields'}, 404

        ids = post_data['meal_ids']
        menuname = post_data['menu_name']

        if not ids:
            return {"message": "Please enter an id to add your meals to the menu"}, 400

        if not isinstance(ids, list):
            return {'message': 'Please enter list id values for meals'}, 400

        for i in ids:
            if not isinstance(i, int):
                return {"message": "List values should only be in numbers"}, 400
            if i < 1:
                return {'message': 'The id should not be 0 or a negative'}, 400

        if not menuname:
            return {'message': 'Please enter the Menu name'}, 400

        if not isinstance(menuname, str):
            return {'message': 'Please enter a string value for Menu name'}, 400

        if len(menuname.strip()) < len(menuname):
            return {'message': 'Menu name should not have spaces!'}, 400

        meal_ids = ids
        menu_meals = []
        for i in meal_ids:
            meal = Meals.query.filter_by(id=i).first()
            if not meal:
                return {"message": "The meal was not found"}, 404
            menu_meals.append(meal)

        menu = Menu.query.filter_by(menu_name=menuname).first()
        if menu:
            return {'message': "Menu already available!"}, 400

        new_menu = Menu(menu_name=menuname)
        new_menu.save()
        new_menu = Menu.query.filter_by(id=new_menu.id).first()
        new_menu.meals.extend(menu_meals)
        new_menu.save()

        output = []
        for meal_in in new_menu.meals:
            menu_data = {}
            menu_data['menu_name'] = meal_in.meal_name
            menu_data['menu_price'] = meal_in.meal_price
            output.append(menu_data)

        return {"status": "success", 'message': 'New menu created!', "data":
                {"Id": new_menu.id, "Menu": new_menu.menu_name, "Meals": output}}, 201


class OrdersAll(Resource):
    """docstring for Orders"""

    @token_required
    def get(self, active_user):
        date = datetime.datetime.utcnow().date()
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        user_det = jwt.decode(token, getenv('SECRET_KEY'))

        orders = Orders.query.filter_by(order_date=str(
            date), order_by=user_det['user_id']).all()

        if not orders:
            return {"message": "You have no order for today"}, 204
        output = []
        for order in orders:
            order_data = {}
            order_data['id'] = order.id
            order_data['meal_name'] = order.order_meal
            order_data['meal_price'] = order.order_price
            order_data['order date'] = order.order_date
            order_data['order time'] = order.order_time
            order_data['quantity'] = order.quantity
            output.append(order_data)

        return {"status": "success", "data": {"My orders": output}}, 200
