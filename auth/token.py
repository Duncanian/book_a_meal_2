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

		if 'Authorization' in request.headers:
			token = request.headers['Authorization']

		if not token:
			return { "message" : "Token is missing!" }, 401
		
		try:
			active_user = jwt.decode(token, getenv('SECRET_KEY'))
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

		if not token:
			return { "message" : "Token is missing!" }, 401
		
		try:
			active_user = jwt.decode(token, getenv('SECRET_KEY'))
		except:
			return {"message":"Token is Invalid!"}, 401

		if not active_user['admin']:
			return "You are not the admin"

		return f(active_user, *args, **kwargs)

	return decorated