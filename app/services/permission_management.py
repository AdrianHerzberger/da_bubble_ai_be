from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from ..configuartions.permissions import PERMISSIONS
from ..storage.permission_data_manager import PermissionDataManager
from ..storage.user_data_manager import UserDataManager


class PermissionManagment:
    _instance = None

    def __init__(self):
        self.permissions_array = PERMISSIONS
        self.permission_data_manager = PermissionDataManager()
        self.user_data_manager = UserDataManager()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PermissionManagment, cls).__new__(
                cls, *args, **kwargs
            )
        return cls._instance


permissions_managment = PermissionManagment()

def permission_required(*required_permissions):
    
    def decorator(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            try:
                user_id = get_jwt_identity()

                if not user_id:
                    return jsonify({"error": "Invalid user ID in JWT"}), 403

                user_data = await permissions_managment.user_data_manager.get_user_by_id(user_id)
                if not user_data:
                    return jsonify({"error": "User not found"}), 404

                if not user_data.permission_id:
                    return jsonify({"error": "User has no permission assigned"}), 403

                permissions = await permissions_managment.permission_data_manager.get_all_permissions()
                if not permissions:
                    return jsonify({"error": "No permissions found"}), 500

                active_permissions = [permission for permission in permissions if permission.active]

                user_permissions = [
                    permission for permission in active_permissions if permission.id
                ]

                validate_permission_slugs = [
                    permission.slug for permission in user_permissions 
                    if permission.slug in permissions_managment.permissions_array
                ]

                if not any(slug in required_permissions for slug in validate_permission_slugs):
                    return jsonify({"error:" "Access forbidden: insufficant permission assignment"}), 403
                
                return await fn(*args, **kwargs)

            except Exception as e:
                return jsonify({"error": f"Error validating permissions: {str(e)}"}), 500

            
        return wrapper
    return decorator
            
