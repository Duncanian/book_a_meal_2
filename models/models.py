from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class BaseModel(db.Model):
    '''Base model to be inherited  by other modells'''
    __abstract__ = True

    def save(self):
        '''save object'''
        try:
            db.session.add(self)
            db.session.commit()
            return None
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Save operation not successful',
                'error': str(e)
            }

    def delete(self):
        '''delete object'''
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Delete operation failed',
                'error': str(e)
            }

class User(BaseModel):
    """docstring for Users"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.id)


class Meals(BaseModel):
    """docstring for Meals"""
    __tablename__ = "meals"
    id = db.Column(db.Integer, primary_key=True)
    meal_name = db.Column(db.String(50))
    meal_price = db.Column(db.Integer)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=True)

    def __repr__(self):
        return '<Meals {}>'.format(self.id)


class Menu(BaseModel):
    """docstring for Meals"""
    __tablename__ = "menu"
    id = db.Column(db.Integer, primary_key=True)
    menu_name = db.Column(db.String(50))
    menu_date = db.Column(db.String, default=datetime.utcnow().date())
    meals = db.relationship('Meals', backref='meals', uselist=True, lazy=True)

    def __repr__(self):
        return '<Menu {}>'.format(self.id)


class Orders(BaseModel):
    """docstring for Orders"""
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    order_meal = db.Column(db.String(50))
    order_price = db.Column(db.Integer)
    order_date = db.Column(db.String, default=datetime.utcnow().date())
    order_time = db.Column(db.String, default=datetime.utcnow().time())
    qty = db.Column(db.Integer)
    order_by = db.Column(db.Integer)

    def __repr__(self):
        return '<Orders {}>'.format(self.id)
