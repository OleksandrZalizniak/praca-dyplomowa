from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from app.auth import authenticate
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    verify_jwt_in_request,
    exceptions as jwt_exceptions
)

api = Blueprint("api", __name__)

@api.route("/", methods=["GET"])
def index():
    return {"status": "API is running"}, 200


@api.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)
    errors = []

    if not data:
        return {"msg": "Invalid input: JSON required"}, 400

    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username:
        errors.append("Username cannot be empty")
    if not password:
        errors.append("Password cannot be empty")
    if password and len(password) < 6:
        errors.append("Password too short (min 6 characters)")
    if username and User.query.filter_by(username=username).first():
        errors.append("Username already exists")

    if errors:
        return {"errors": errors}, 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return {"msg": "User created"}, 201


@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return {"msg": "Username and password required"}, 400

    token = authenticate(data["username"], data["password"])
    if not token:
        return {"msg": "Bad credentials"}, 401

    return {"access_token": token}, 200


@api.route("/profile", methods=["GET"])
def profile():
    try:
        verify_jwt_in_request()
    except jwt_exceptions.NoAuthorizationError:
        return {"msg": "Missing JWT token"}, 401
    except jwt_exceptions.ExpiredSignatureError:
        return {"msg": "Token has expired"}, 401
    except (jwt_exceptions.JWTDecodeError, jwt_exceptions.InvalidHeaderError):
        return {"msg": "Invalid JWT token"}, 422
    except Exception:
        return {"msg": "Invalid JWT"}, 422

    current_user = get_jwt_identity()
    return {
        "message": "Access granted",
        "user": current_user
    }, 200
