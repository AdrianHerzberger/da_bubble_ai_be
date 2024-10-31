from flask import Blueprint, jsonify, request
from ..storage.user_data_manager import UserDataManager
from ..instances.db_instance import db
from flask_jwt_extended import create_access_token, set_access_cookies, get_jwt, get_jwt_identity, jwt_required

from datetime import datetime, timedelta, timezone

user_routes = Blueprint("user_routes", __name__)
user_data_manager = UserDataManager(db)


@user_routes.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


@user_routes.route("/get_user_by_id/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = user_data_manager.get_user_by_id(user_id)

    try:
        if user:
            return jsonify({
                "user_id": user.id,
                "user_name": user.user_name,
                "user_email": user.user_email,
                "user_profile_picture_url": user.user_profile_picture_url
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error getting user data by id: {e}")
        return jsonify({"error": "Failed to get user data by id"}), 500


@user_routes.route("/get_user_by_email/<user_email>", methods=["GET"])
def get_user_by_email(user_email):
    user = user_data_manager.get_user_by_email(user_email)
    try:
        if user:
            return jsonify({
                "user_id": user.id,
                "user_name": user.user_name,
                "user_email": user.user_email,
                "user_profile_picture_url": user.user_profile_picture_url
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error getting user data by email: {e}")
        return jsonify({"error": "Failed to get user data by email"}), 500


@user_routes.route("/all_users", methods=["GET"])
def get_all_user():
    users = user_data_manager.get_all_users()

    try:
        if users:
            user_list = []
            for user in users:
                user_data = {
                    "user_id": user.id,
                    "user_name": user.user_name,
                    "user_email": user.user_email,
                    "user_profile_picture_url": user.user_profile_picture_url
                }
                user_list.append(user_data)
            return jsonify(user_list), 200
        else:
            return jsonify({"error": "Users not found"}), 404
    except Exception as e:
        print(f"Error getting all user data: {e}")
        return jsonify({"error": "Failed to get all user data"}), 500


@user_routes.route("/register_user", methods=["POST"])
def register_user():
    data = request.get_json()
    user_email = data.get('user_email')
    user_name = data.get('user_name')
    user_password = data.get('user_password')

    try:
        new_user = user_data_manager.create_user(
            user_email, user_name, user_password)
        print(f"Result if user: {new_user}")
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({"error": "Failed to create user"}), 500


@user_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user_email = data.get("user_email")
    user_password = data.get("user_password")
    user_profile_picture_url = data.get("user_profile_picture_url")
    user = user_data_manager.get_user_by_email(user_email)

    response = jsonify({"msg": "login successful"})

    try:
        if user and user_data_manager.check_user_password(user_password, user.user_password):
            user_data_manager.update_user_profile_picture(
                user.id, user_profile_picture_url)
            access_token = create_access_token(identity=user.id,  expires_delta=timedelta(hours=1))
            set_access_cookies(response, access_token)
            return jsonify({
                "message": "Sign-in successfully",
                "user_id": user.id,
                "user_name": user.user_name,
                "user_profile_picture_url": user.user_profile_picture_url,
                "access_token": access_token
            }), 201
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({"error": "Failed to login user"}), 500


@user_routes.route("/logout")
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@user_routes.route("/protected")
@jwt_required()
def protected():
    return jsonify(foo="bar")
