#!/usr/bin/env python3

<<<<<<< HEAD
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Local imports
from config import app, db
from routes.auth_routes import auth_bp  # auth blueprint

# Database & migration setup
migrate = Migrate(app, db)

# JWT setup
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp)

# Root route
@app.route("/")
def index():
    return "<h1>Project Server Running...</h1>"

# Run app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # optional; Flask-Migrate handles migrations
    app.run(port=5555, debug=True)


=======
# -----------------------------
# REMOTE LIBRARY IMPORTS
# -----------------------------
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_migrate import Migrate

# -----------------------------
# LOCAL IMPORTS
# -----------------------------
from config import app  # make sure config.py creates 'app' and 'db'
from models.user import User

# -----------------------------
# DATABASE SETUP
# -----------------------------
# If you haven’t already, set up SQLAlchemy in config.py:
# db = SQLAlchemy(app)
from config import db

# Setup Flask-Migrate
migrate = Migrate(app, db)

# -----------------------------
# JWT SETUP
# -----------------------------
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # replace with env var in production
jwt = JWTManager(app)

# -----------------------------
# ROUTES
# -----------------------------
@app.route('/')
def index():
    return '<h1>Project Server Running...</h1>'

# SIGNUP
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 400

    new_user = User(username=username, email=email, household_id=1)  # default household
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    token = create_access_token(identity=new_user.id)
    return jsonify({
        "token": token,
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
    }), 201

# LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 200

# CURRENT USER
@app.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # optional; Flask-Migrate will handle migrations
    app.run(port=5555, debug=True)
>>>>>>> development
