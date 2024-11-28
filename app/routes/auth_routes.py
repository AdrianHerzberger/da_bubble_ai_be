import asyncio
from flask import Blueprint, jsonify, request
from ..utils.auth_helper import generate_tokens
from ..storage.user_data_manager import UserDataManager
from flask_jwt_extended import (create_access_token, create_refresh_token, 
                                get_jwt, set_access_cookies, set_refresh_cookies, 
                                jwt_required, get_jwt_identity, unset_jwt_cookies)

from datetime import datetime, timedelta, timezone

auth_routes = Blueprint("auth_routes", __name__)
user_data_manager = UserDataManager()

@auth_routes.route("/login", methods=["POST"])
async def login():
    data = request.get_json()
    user_email = data.get("user_email")
    user_password = data.get("user_password")
    user = await user_data_manager.get_user_by_email(user_email)
    
    last_login_date = datetime.now()
    user_id = user.id

    try:
        if user and user_data_manager.check_user_password(user_password, user.user_password):
            access_token = create_access_token(
                identity=user.id, expires_delta=timedelta(minutes=30))
            
            refresh_token = create_refresh_token(
                identity=user.id)
            
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
    
    
@auth_routes.route("/current_user", methods=["GET"])
@jwt_required()
async def current_user():
    try:
        user_id = get_jwt_identity()
        user = await user_data_manager.get_user_by_id(user_id)
        return jsonify({
            "user_id": user.id,
            "user_name": user.user_name,
            "email": user.user_email
        }), 200
    except Exception as e:
        print(f"Error getting current user token: {e}")
        return jsonify({"error": "Failed to get current user"}), 500

    
@auth_routes.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        user_id = get_jwt_identity()
        new_access_token, _ = generate_tokens(user_id) 
        response = jsonify({
            "message": "Token refreshed successfully",
            "access_token": new_access_token
        })

        set_access_cookies(response, new_access_token)
        return response, 200
    except Exception as e:
        print(f"Error refreshing token: {e}")
        return jsonify({"error": "Failed to refresh token"}), 500
    

@auth_routes.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response


@auth_routes.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(message="Access granted to protected resource"), 200


