import asyncio
from ..instances.create_async_engine import AsyncSessionLocal
from ..models.role_permission_model import RolePermissionAssociation
from ..models.role_model import Role
from ..models.permission_model import Permission
from ..repository_manager.role_permission_association_data_manager_interface import RolePermissionAssociationDataManagerInterface
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select 
from sqlalchemy import and_ 


class RolePermissionAssociationDataManager(RolePermissionAssociationDataManagerInterface):
    def __init__(self):
        self.db_session_factory = AsyncSessionLocal
              
    async def create_role_permission_association(self, role_id, permission_id):
        async with self.db_session_factory() as session:
            try:
                exitsting_association_query = select(RolePermissionAssociation).filter(
                    and_(
                        RolePermissionAssociation.role_id == role_id,
                        RolePermissionAssociation.permission_id == permission_id
                    )
                )
                
                association_result = await session.execute(exitsting_association_query)
                existing_association = association_result.scalar_one_or_none()
                
                if existing_association:
                    print(f"Association between role {role_id} and permission {permission_id} already existis")
                    return
                
                new_role_permission_association = RolePermissionAssociation(
                    role_id=role_id,
                    permission_id=permission_id
                )
                
                session.add(new_role_permission_association)
                await session.commit()
                await session.refresh(new_role_permission_association)
                return new_role_permission_association
            except Exception as e:
                print(f"Error creating role permission association")
                await session.rollback()
                return False
            
    async def get_roles_for_permissions(self, permission_id):
        async with self.db_session_factory() as session:
            try:
                role_query = select(Role).join(RolePermissionAssociation).filter(
                    RolePermissionAssociation.permission_id == permission_id
                )
                
                role_result = await session.execute(role_query)
                roles = role_result.scalars().all()
                print(f"Roles from the query : {roles}")
                
                role_for_permission = [
                    {
                        "role_id": role.id,
                        "title": role.title,
                        "slug": role.slug
                    }
                    for role in roles
                ]
                return role_for_permission
            except Exception as e:
                print(f"Error getting roles for permission {permission_id}: {e}")
                return None
            
    async def get_permission_for_roles(self, role_id):
        async with self.db_session_factory() as session:
            try:
                permission_query = select(Permission).join(RolePermissionAssociation).filter(
                    RolePermissionAssociation.role_id == role_id
                )
                
                permission_result = await session.execute(permission_query)
                permissions = permission_result.scalars().all()
                print(f"Permissions from the query : {permissions}")
                
                permission_for_roles = [
                    {
                        "role_id": permission.id,
                        "title": permission.title,
                        "slug": permission.slug
                    }
                    for permission in permissions
                ]
                return permission_for_roles
            except Exception as e:
                print(f"Error getting permission for roles {role_id}: {e}")
                return None
            