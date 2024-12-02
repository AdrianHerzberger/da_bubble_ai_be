import asyncio
from flask import Blueprint, jsonify, request
from ..storage.user_data_manager import UserDataManager

user_routes = Blueprint("user_routes", __name__)
user_data_manager = UserDataManager()

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
        return jsonify(new_user), 201
    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({"error": "Failed to create user"}), 500





