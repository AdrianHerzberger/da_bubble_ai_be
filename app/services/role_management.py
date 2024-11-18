from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from ..configuartions.roles import ROLES
from ..storage.role_data_manager import RoleDataManager
from ..storage.user_data_manager import UserDataManager


class RoleManagement:
    _instance = None

    def __init__(self):
        self.roles_array = ROLES
        self.role_data_manager = RoleDataManager()
        self.user_data_manager = UserDataManager()
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RoleManagement, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance
    
role_management = RoleManagement()

def role_required(*required_roles):
    
    def decorator(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            try:
                user_id = get_jwt_identity()
                
                if not user_id:
                    return jsonify({"error": "Invalid user ID in JWT"}), 403
                
                user_data = await role_management.user_data_manager.get_user_by_id(user_id)
                if not user_data:
                    return jsonify({"error": "User not found"}), 404
                
                user_role_ids = user_data.role_id
                if not user_role_ids:
                    return jsonify({"error": "User has no roles assigned"}), 403
                
                roles = await role_management.role_data_manager.get_all_roles()
                if not roles:
                    return jsonify({"error": "No roles found"}), 500
                
                active_roles = [role for role in roles if role.active] 
                
                user_roles = [
                    role for role in active_roles if role.id
                ]

                valid_role_slugs = [
                    role.slug for role in user_roles if role.slug in role_management.roles_array
                ]
                
                if not any(slug in required_roles for slug in valid_role_slugs):
                    return jsonify({"error": "Access forbidden: insufficant role assignment"}), 403

                return await fn(*args, **kwargs)
            
            except Exception as e:
                return jsonify({"error": f"Error validating roles: {str(e)}"}), 500
            
        return wrapper
    return decorator
        
        
        
 