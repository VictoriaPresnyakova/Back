from functools import wraps
from flask import request, jsonify
from utils.jwt_helper import decode_token

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token:
            token = token.replace("Bearer ", "")
        user_id = decode_token(token)
        if not user_id:
            return jsonify({"message": "Invalid or missing token"}), 401
        return f(user_id=user_id, *args, **kwargs)
    return decorated_function
