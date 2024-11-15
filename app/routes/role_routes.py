import asyncio
from flask import Blueprint, jsonify, request
from ..storage.role_data_manager import RoleDataManager

role_routes = Blueprint("role_routes", __name__)
role_data_manager = RoleDataManager()

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
    except  Exception as e:
        print(f"Error getting role data by id: {e}")
        return jsonify({"error": "Failed to get role data by id"}), 500