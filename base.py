from flask import Flask
from flask_restful import Api
from app import Hello
from views.user_res import AuthCreate, AuthLogin, MenuOrders, Profile
from views.cater_res import MealMan, Menus, OrdersAll
from config import config


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    api = Api(app)

    from models.models import db
    db.init_app(app)

    api.add_resource(Hello, '/')

    api.add_resource(AuthCreate, '/api/v2/auth/signup',
                     '/api/v2/auth/signup/', '/api/v2/users', '/api/v2/users/')

    api.add_resource(AuthLogin, '/api/v2/auth/login', '/api/v2/auth/login/')

    api.add_resource(Profile, '/api/v2/profile', '/api/v2/profile/')

    api.add_resource(MealMan, '/api/v2/meals/', '/api/v2/meals', '/api/v2/meals/', '/api/v2/meals', '/api/v2/meals/<int:meal_id>',
                     '/api/v2/meals/<int:meal_id>/', '/api/v2/meals/<int:meal_id>', '/api/v2/meals/<int:meal_id>/')

    api.add_resource(Menus, '/api/v2/menu/', '/api/v2/menu')

    api.add_resource(OrdersAll, '/api/v2/orders', '/api/v2/orders/')

    api.add_resource(MenuOrders, '/api/v2/menu/', '/api/v2/menu', '/api/v2/orders', '/api/v2/orders/',
                                 '/api/v2/orders/<int:order_id>', '/api/v2/orders/<int:order_id>/',
                                 '/api/v2/orders/<int:order_id>', '/api/v2/orders/<int:order_id>/')

    return app


app = create_app(config['development'])
