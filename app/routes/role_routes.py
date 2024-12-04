import asyncio
from flask import Blueprint, jsonify, request
from ..storage.role_data_manager import RoleDataManager
from ..storage.user_data_manager import UserDataManager

role_routes = Blueprint("role_routes", __name__)
role_data_manager = RoleDataManager()
user_data_manager = UserDataManager()


@role_routes.route("/create_role", methods=["POST"])
async def create_role():
    data = request.get_json()
    title = data.get("title")
    slug = data.get("slug")
    description = data.get("description")
    active = data.get("active")
    context = data.get("context")

    try:
        new_role = await role_data_manager.create_role(
            title, slug, description, active, context
        )
        return jsonify({"message": "Role created successfully"}), 201
    except Exception as e:
        print(f"Error creating role: {e}")
        return jsonify({"error": "Failed to create role"}), 500


@role_routes.route("/get_role_by_id/<int:role_id>", methods=["GET"])
async def get_role_by_id(role_id):
    try:
        role = await role_data_manager.get_role_by_id(role_id)
        if role:
            return jsonify({
                "title": role.title,
                "slug": role.slug,
                "description": role.description,
                "context": role.context,
            }), 200
        else:
            return jsonify({"error": "Role not found"}, 404)
    except Exception as e:
        print(f"Error getting role data by id: {e}")
        return jsonify({"error": "Failed to get role data by id"}), 500


@role_routes.route("/get_all_roles/", methods=["GET"])
async def get_all_roles():
    try:
        roles = await role_data_manager.get_all_roles()
        if roles:
            role_list = []
            for role in roles:
                role_data = {
                    "role_id": role.id,
                    "title": role.title,
                    "slug": role.slug,
                    "description": role.description,
                    "active": role.active,
                    "context": role.context,
                }
                role_list.append(role_data)
            return jsonify(role_list), 200
        else:
            return jsonify({"error": "Roles not found"}), 404
    except Exception as e:
        print(f"Error getting all role data: {e}")
        return jsonify({"error": "Failed to get all roles"}, 500)


@role_routes.route("/assign_role", methods=["POST"])
async def assign_role():
    data = request.get_json()
    user_id = data.get("user_id")
    role_id = data.get("role_id")

    if not user_id or not role_id:
        return {"error": "user_id and role_id are required"}, 400

    try:
        user = await user_data_manager.get_user_by_id(user_id)
        role = await role_data_manager.get_role_by_id(role_id)

        if not user:
            return jsonify({"error": "User not found"}), 400
        if not role:
            return jsonify({"error": "Role not found"}), 400

        user_role_assigment = await role_data_manager.assign_role_to_user(user_id, role_id)
        
        if user_role_assigment:
            return jsonify({"message": f"Role '{role.title}' assigned to user '{user.user_name}' successfully"}), 200
        else:
            return jsonify({"error": "Failed to assign role to user"}), 404
    except Exception as e:
        print(f"Error assigning role: {e}")
        return jsonify({"error": "An error occurred while assigning role"}), 500
