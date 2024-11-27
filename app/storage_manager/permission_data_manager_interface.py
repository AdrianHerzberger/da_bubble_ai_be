from abc import ABC, abstractclassmethod

class PermissionDataManagerInterface(ABC):
    @abstractclassmethod
    def create_permission(self, title, slug, description, active, context):
        pass
    
    @abstractclassmethod
    def get_all_permissions(self):
        pass
    
    @abstractclassmethod
    def get_permission_by_id(self, permission_id):
        pass