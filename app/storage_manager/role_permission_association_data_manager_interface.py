from abc import ABC, abstractclassmethod

class RolePermissionAssociationDataManagerInterface(ABC):
    @abstractclassmethod
    def create_role_permission_association(self, role_id, permission_id):
        pass
    
    @abstractclassmethod
    def get_roles_for_permissions(self, permission_id):
        pass
    
    @abstractclassmethod
    def get_permission_for_roles(self, role_id):
        pass