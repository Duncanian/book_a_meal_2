from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from datetime import datetime

class User(db.Model):
	"""docstring for Users"""
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(50))
	password = db.Column(db.String(80))
	admin = db.Column(db.Boolean)

	def __repr__(self):
		return '<User {}>'.format(self.id)

class Meals(db.Model):
	"""docstring for Meals"""
	__tablename__ = "meals"
	id = db.Column(db.Integer, primary_key = True)
	meal_name = db.Column(db.String(50))
	meal_price = db.Column(db.Integer)
	menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=True)

	def __repr__(self):
		return '<Meals {}>'.format(self.id)

class Menu(db.Model):
	"""docstring for Meals"""
	__tablename__ = "menu"
	id = db.Column(db.Integer, primary_key = True)
	menu_name = db.Column(db.String(50))
	menu_date = db.Column(db.String, default=datetime.utcnow().date())
	meals = db.relationship('Meals', backref='meals', uselist=True, lazy=True)

	def __repr__(self):
		return '<Menu {}>'.format(self.id)

class Orders(db.Model):
	"""docstring for Orders"""
	__tablename__ = "orders"
	id = db.Column(db.Integer, primary_key = True)
	order_meal = db.Column(db.String(50))
	order_price = db.Column(db.Integer)
	time_ordered = db.Column(db.String, default=datetime.utcnow().date())
	qty = db.Column(db.Integer)
	order_by= db.Column(db.Integer)

	def __repr__(self):
		return '<Orders {}>'.format(self.id)
