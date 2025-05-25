from flask import Blueprint, request, jsonify
from app.dao.user_dao import UserDAO
from app.models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from utils.jwt_helper import encode_token
from app.database import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already exists"}), 400
    hashed_pw = generate_password_hash(data["password"])
    user = User(name=data["name"], email=data["email"], jwt_token=None, password_hash=hashed_pw)
    db.session.add(user) #TODO
    db.session.commit()
    return jsonify({"message": "Registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if user and check_password_hash(user.password_hash, data["password"]):  # <- user.jwt_token not ideal
        token = encode_token(user.id)
        user.jwt_token = token  # можно хранить в БД
        db.session.commit()
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401
