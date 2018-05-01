from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
	"""docstring for Users"""
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.String(50), unique = True)
	username = db.Column(db.String(50))
	password = db.Column(db.String(80))
	admin = db.Column(db.Boolean)

	def __init__(self, user_id, username, password, admin):
		self.user_id = user_id
		self.username = username
		self.password = password
		self.admin = admin

	def __repr__(self):
		return '<User {}>'.format(self.user_id)

class Meals(db.Model):
	"""docstring for Meals"""
	__tablename__ = "meals"
	id = db.Column(db.Integer, primary_key = True)
	meal_id = db.Column(db.String(50), unique = True)
	meal_name = db.Column(db.String(50))
	meal_price = db.Column(db.Float)
	meal_category = db.Column(db.String(50))
	meal_day = db.Column(db.String(50))

	def __init__(self, meal_id, meal_name, meal_price, meal_category, meal_day):
		self.meal_id = meal_id
		self.meal_name = meal_name
		self.meal_price = meal_price
		self.meal_category = meal_category
		self.meal_day = meal_day

	def __repr__(self):
		return '<Meals {}>'.format(self.meal_id)

class Menu(db.Model):
	"""docstring for Meals"""
	__tablename__ = "menu"
	id = db.Column(db.Integer, primary_key = True)
	menu_id = db.Column(db.String(50), unique = True)
	menu_name = db.Column(db.String(50))
	menu_price = db.Column(db.Float)
	menu_category = db.Column(db.String(50))
	menu_day = db.Column(db.String(50))

	def __init__(self, menu_id, menu_name, menu_price, menu_category, menu_day):
		self.menu_id = menu_id
		self.menu_name = menu_name
		self.menu_price = menu_price
		self.menu_category = menu_category
		self.menu_day = menu_day

	def __repr__(self):
		return '<Menu {}>'.format(self.menu_id)

class Orders(db.Model):
	"""docstring for Orders"""
	__tablename__ = "orders"
	id = db.Column(db.Integer, primary_key = True)
	order_id = db.Column(db.String(50), unique = True)
	order_name = db.Column(db.String(50))
	order_price = db.Column(db.Float)
	order_category = db.Column(db.String(50))
	order_day = db.Column(db.String(50))
	order_qty = db.Column(db.Integer)
	order_user = db.Column(db.String(50))

	def __init__(self, order_id, order_name, order_price, order_category, order_day, order_qty, order_user):
		self.order_id = order_id
		self.order_name = order_name
		self.order_price = order_price
		self.order_category = order_category
		self.order_day = order_day
		self.order_qty = order_qty
		self.order_user = order_user

	def __repr__(self):
		return '<Orders {}>'.format(self.order_id)
