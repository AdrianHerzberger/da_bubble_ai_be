import asyncio
from flask import Blueprint, jsonify, request
from ..storage.user_data_manager import UserDataManager
from ..storage.role_data_manager import RoleDataManager
from flask_jwt_extended import (create_access_token, create_refresh_token, 
                                get_jwt, set_access_cookies, set_refresh_cookies, 
                                jwt_required, get_jwt_identity, unset_jwt_cookies)
from datetime import datetime, timedelta, timezone

user_routes = Blueprint("user_routes", __name__)
user_data_manager = UserDataManager()
role_data_manager = RoleDataManager()


@user_routes.route("/get_user_by_id/<user_id>", methods=["GET"])
async def get_user_by_id(user_id):
    try:
        user = await user_data_manager.get_user_by_id(user_id)
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
async def get_user_by_email(user_email):
    try:
        user = await user_data_manager.get_user_by_email(user_email)
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


@user_routes.route("/get_all_users", methods=["GET"])
async def get_all_user():
    try:
        users = await user_data_manager.get_all_users()           
        if users:
            user_list = []
            for user in users:
                user_data = {
                    "user_id": user.id,
                    "user_name": user.user_name,
                    "user_email": user.user_email,
                    "user_profile_picture_url": user.user_profile_picture_url,
                    "role_id": user.role_id
                }
                user_list.append(user_data)
            return jsonify(user_list), 200
        else:
            return jsonify({"error": "Users not found"}), 404
    except Exception as e:
        print(f"Error getting all user data: {e}")
        return jsonify({"error": "Failed to get all user data"}), 500


@user_routes.route("/register_user", methods=["POST"])
async def register_user():
    data = request.get_json()
    user_email = data.get('user_email')
    user_name = data.get('user_name')
    user_password = data.get('user_password')

    try:
        new_user = await user_data_manager.create_user(
            user_email, user_name, user_password)
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({"error": "Failed to create user"}), 500


@user_routes.route("/login", methods=["POST"])
async def login():
    data = request.get_json()
    user_email = data.get("user_email")
    user_password = data.get("user_password")
    user = await user_data_manager.get_user_by_email(user_email)
    
    last_login_date = datetime.today().strftime('%Y-%m-%d')
    user_id = user.id

    try:
        if user and user_data_manager.check_user_password(user_password, user.user_password):
            access_token = create_access_token(
                identity=user.id, expires_delta=timedelta(minutes=30))
            
            refresh_token = create_access_token(
                identity=user.id, expires_delta=timedelta(minutes=30))
            
            await user_data_manager.update_user_last_login_date(user_id, last_login_date)
            
            response = jsonify({
                "message": "Login successful",
                "user_id": user.id,
                "user_name": user.user_name,
                "access_token": access_token,
                "refresh_token": refresh_token
            })
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            
            return response, 201
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"error": "Failed to login user"}), 500


@user_routes.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        user_id = get_jwt_identity()
        new_access_token = create_access_token(
            identity=user_id, expires_delta=timedelta(minutes=30))

        response = jsonify({
            "message": "Token refreshed successfully",
            "access_token": new_access_token
        })

        set_access_cookies(response, new_access_token)
        return response, 200
    except Exception as e:
        print(f"Error refreshing token: {e}")
        return jsonify({"error": "Failed to refresh token"}), 500


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


@user_routes.route("/logout")
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@user_routes.route("/protected")
@jwt_required()
def protected():
    return jsonify(foo="bar")
