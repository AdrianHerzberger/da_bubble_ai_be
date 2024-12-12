import asyncio
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..storage.user_data_manager import UserDataManager
from ..services.permission_management import permission_required

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


@user_routes.route("/delete_user/<user_id>", methods=["DELETE"])
@jwt_required()
@permission_required("manage-users")
async def delete_user(user_id):
    try:
        user_auth = get_jwt_identity()
        if not user_auth:
            return jsonify({"error": "User authentication not valid!"}), 401
        delete_user = await user_data_manager.delete_user(user_id)
        if delete_user:
            return jsonify({"success": "User deleted successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404 
    except Exception as e:
        print(f"Error deleting user data: {e}")
        return jsonify({"error": "Failed to delete user data"}), 500


@user_routes.route("/update_user/<user_id>", methods=["PATCH"])
@jwt_required()
@permission_required("generell")
async def update_user(user_id):
    data = request.get_json()
    user_name_update = data.get("update_user_name")

    try:
        user_auth = get_jwt_identity()
        if not user_auth:
            return jsonify({"error": "User authentication not valid!"}), 401
        update_user_name = await user_data_manager.update_user(user_id, user_name_update)
        if update_user_name:
            return jsonify({"message": "User updated successfully"}), 200
        else:
            return jsonify({"error": "User not found"})
    except Exception as e:
        print(f"Error updating user  data: {e}")
        return jsonify({"error": "Failed to update user data"}), 500


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





