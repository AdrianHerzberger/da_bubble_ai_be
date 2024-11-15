import asyncio
from flask import Blueprint, jsonify, request
from ..storage.permission_data_manager import PermissionDataManager

permission_routes =  Blueprint("permission_routes", __name__)
permission_data_manager = PermissionDataManager()


@permission_routes.route("/create_permission", methods=["POST"])
async def create_permission():
    data = request.get_json()
    title = data.get("title")
    slug = data.get("slug")
    description = data.get("description")
    active = data.get("active")
    context = data.get("context")

    try:
        new_permission = await permission_data_manager.create_permission(
            title, slug, description, active, context
        )
        return jsonify({"message": "Permission created successfully"}), 201
    except Exception as e:
        print(f"Error creating permission: {e}")
        return jsonify({"error": "Failed to create permission"}), 500
    

@permission_routes.route("/get_permission_by_id/<int:permission_id>", methods=["GET"])
async def get_permission_by_id(permission_id):
    try:
        permission = await permission_data_manager.get_permission_by_id(permission_id)
        if permission:
            return jsonify({
                "title": permission.title,
                "slug": permission.slug,
                "description": permission.description,
                "context": permission.context,
            }), 200
        else:
            return jsonify({"error": "Permission not found"}, 404)
    except Exception as e:
        print(f"Error getting permission data by id: {e}")
        return jsonify({"error": "Failed to get permission data by id"}), 500


@permission_routes.route("/get_all_permissions/", methods=["GET"])
async def get_all_roles():
    try:
        permissions = await permission_data_manager.get_all_permissions()
        if permissions:
            permission_list = []
            for permission in permissions:
                permission_data = {
                    "role_id": permission.id,
                    "title": permission.title,
                    "slug": permission.slug,
                    "description": permission.description,
                    "active": permission.active,
                    "context": permission.context,
                }
                permission_list.append(permission_data)
            return jsonify(permission_list), 200
        else:
            return jsonify({"error": "Permissions not found"}), 404
    except Exception as e:
        print(f"Error getting all permission data: {e}")
        return jsonify({"error": "Failed to get all ermissions"}, 500)