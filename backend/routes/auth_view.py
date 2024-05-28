from flask import request, jsonify
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from db import db

bcrypt = Bcrypt()
jwt = JWTManager()


class SignupView(MethodView):
    def __init__(self) -> None:
        self.collection = db['users']

    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        print(username, password)
        if not username or not password:
            return jsonify({"error": "please enter a valid username and password"}), 400

        existing_user = self.collection.find_one({"username": username})
        if existing_user:
            return jsonify({"error": "user already exists"}), 400

        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        user = {'username': username, 'password': hashed_password}
        self.collection.insert_one(user)

        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 201


class LoginView(MethodView):
    def __init__(self) -> None:
        self.collection = db['users']

    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = self.collection.find_one({'username': username})
        if not user or not bcrypt.check_password_hash(user['password'], password):
            return jsonify({'error': 'Invalid username or password'}), 401

        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200


class ProtectedView(MethodView):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return jsonify({'message': f'Hello, {current_user}! This is a protected endpoint.'}), 200


