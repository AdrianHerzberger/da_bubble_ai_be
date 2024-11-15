from abc import ABC, abstractclassmethod

class RoleDataManagerInterface(ABC):
    @abstractclassmethod
    def create_role(self, title, slug, description, active, context):
        pass
    
    @abstractclassmethod
    def get_all_roles(self):
        pass
    
    @abstractclassmethod
    def get_role_by_id(self, role_id):
        pass