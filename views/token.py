from functools import wraps
from os import getenv
from models.models import User
from flask import request, jsonify
import jwt
import json

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None

		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']

		if not token:
			return { "message" : "Token is missing!" }, 401
		
		try:
			data = jwt.decode(token, getenv('SECRET_KEY'), algorithm='HS256')
			active_user = User.query.filter_by(user_id = data['user_id']).first()
		except:
			return {"message":"Token is Invalid!"}, 401

		return f(active_user, *args, **kwargs)

	return decorated


def admin_only(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None

		if 'Authorization' in request.headers:
			token = request.headers['Authorization']

		if token is None:
			return jsonify({ "message" : "Token is missing!" }), 401
		
		try:
			data = jwt.decode(token, getenv('SECRET_KEY'))
			active_user = User.query.filter_by(user_id = data['user_id']).first()
		except:
			return jsonify({"message":"Token is Invalid!"}), 400

		'''if not admin_access:
			return jsonify({"message":"You don't have permission to perform this action"})'''

		return f(active_user, *args, **kwargs)

	return decorated