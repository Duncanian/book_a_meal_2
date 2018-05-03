from flask import Flask
from flask_restful import Api
from app import Hello
from views.user_res import AuthCreate, AuthLogin, MenuOrders
from views.cater_res import MealMan, Menu, OrdersAll
from config import config

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    api = Api(app)

    from models.models import db
    db.init_app(app)

    api.add_resource(Hello, '/')
    api.add_resource(AuthCreate, '/api/v1/auth/signup', '/api/v1/users')
    api.add_resource(AuthLogin, '/api/v1/auth/login')
    api.add_resource(MealMan, '/api/v1/meals/', '/api/v1/meals/',
    	                '/api/v1/meals/<string:meal_id>', '/api/v1/meals/<string:meal_id>')
    api.add_resource(Menu, '/api/v1/menu/')
    api.add_resource(OrdersAll, '/api/v1/orders')
    api.add_resource(MenuOrders, '/api/v1/menu/', '/api/v1/orders',
    	                '/api/v1/orders/<int:order_id>', '/api/v1/orders/<int:order_id>')

    return app

app = create_app(config['development'])