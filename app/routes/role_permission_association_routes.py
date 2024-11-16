from flask import Blueprint, jsonify, request
from ..storage.role_permission_data_manager import RolePermissionAssociationDataManager

role_permission_association_routes = Blueprint(
    "role_permission_association_routes", __name__)
role_permission_association_data_manager = RolePermissionAssociationDataManager()

@role_permission_association_routes.route("/create_role_association_to_permission", methods=["POST"])
async def create_role_association_to_permission():
    data = request.get_json()
    role_id = data.get("role_id")
    permission_id = data.get("permission_id")
    
    try:
        new_role_association = await role_permission_association_data_manager.create_role_permission_association(
            role_id, permission_id
        )
        if not new_role_association:
            return jsonify({"error": f"Failed to associate user {role_id} with channel {permission_id}"}), 500

        return jsonify({
            "message": "Role permission association created successfully",
            "role_id": role_id,
            "permission_id": permission_id
        }), 201

    except Exception as e:
        print(f"Error creating role association to permission: {e}")
        return jsonify({"error": "Failed to create role permission association"}), 500
    
    
@role_permission_association_routes.route("/get_roles_for_permissions/<int:permission_id>", methods=["GET"])
async def get_roles_for_permissions(permission_id):
    try:
        roles = await role_permission_association_data_manager.get_roles_for_permissions(permission_id)
        print(f"The result of found roles : {roles}")
        if roles:
            return jsonify(roles), 200
        else:
            return jsonify({"error": "No roles found for this permission"}), 404
    except Exception as e:
        print(f"Error fetching roles for permission: {e}")
        return jsonify({"error": "Failed to fetch roles"}), 500


@role_permission_association_routes.route("/get_permission_for_roles/<int:role_id>", methods=["GET"])
async def get_permission_for_roles(role_id):
    try:
        permissions = await role_permission_association_data_manager.get_permission_for_roles(role_id)
        print(f"The result of found permissions : {permissions}")
        if permissions:
            return jsonify(permissions), 200
        else:
            return jsonify({"error": "No permissions found for this role"}), 404
    except Exception as e:
        print(f"Error fetching permissions for role: {e}")
        return jsonify({"error": "Failed to fetch permissions"}), 500