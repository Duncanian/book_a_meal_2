from functools import wraps
from os import getenv
from models.models import User

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None

		if 'x-access-token' in request.headers:
			token = request.headers['Authorization']

		if not token:
			return jsonify({ "message" : "Token is missing!" }), 401
		
		try:
			data = jwt.decode(token, getenv('SECRET_KEY'))
			active_user = User.query.filter_by(user_id = data['user_id']).first()

		except:
			return jsonify({"message":"Token is Invalid!"}), 400

		return f(current_user, *args, **kwargs)

	return decorated
