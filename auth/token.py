from functools import wraps
import json
from os import getenv
from flask import request, jsonify
import jwt
from models.models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return {"message": "Token is missing!"}, 401

        try:
            active_user = jwt.decode(token, getenv('SECRET_KEY'))
        except:
            return {"message": "Token is Invalid!"}, 400

        return f(active_user, *args, **kwargs)

    return decorated


def admin_only(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return {"message": "Token is missing!"}, 401

        try:
            active_user = jwt.decode(token, getenv('SECRET_KEY'))
        except:
            return {"message": "Token is Invalid!"}, 400

        if not active_user['admin']:
            return {"message": "Sorry, you not authorized to use this endpoint"}, 401

        return f(active_user, *args, **kwargs)

    return decorated
