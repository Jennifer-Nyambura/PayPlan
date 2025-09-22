from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import db, User
from schemas.user_schema import UserSchema

auth_bp = Blueprint("auth_bp", __name__)
user_schema = UserSchema()

# -----------------------------
# SIGNUP
# -----------------------------
@auth_bp.route("/signup", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    household_id = data.get("household_id") or 1

    # Check if user exists by username or email
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "User already exists"}), 400

    # Create new user
    new_user = User(username=username, email=email, household_id=household_id)
    new_user.set_password(password)  # Ensure this method hashes password

    db.session.add(new_user)
    db.session.commit()

    # Create JWT token
    token = create_access_token(identity={"id": new_user.id, "household_id": new_user.household_id})

    return jsonify({
        "access_token": token,
        "user": user_schema.dump(new_user)
    }), 201


# -----------------------------
# LOGIN
# -----------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity={"id": user.id, "household_id": user.household_id})

    return jsonify({
        "access_token": token,
        "user": user_schema.dump(user)
    }), 200


# -----------------------------
# CURRENT USER
# -----------------------------
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    identity = get_jwt_identity()
    user_id = identity.get("id")  # safer access
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return user_schema.dump(user), 200
