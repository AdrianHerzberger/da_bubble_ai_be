import asyncio
from ..instances.create_async_engine import AsyncSessionLocal
from ..models.permission_model import Permission
from ..repository_manager.permission_data_manager_interface import PermissionDataManagerInterface
from sqlalchemy.future import select
import datetime
import random


class PermissionDataManager(PermissionDataManagerInterface):
    def __init__(self):
        self.db_session_factory = AsyncSessionLocal
        
    async def create_permission(self, title, slug, description, active, context):
        created_at = datetime.datetime.utcnow()
        permission_id = random.randint(100, 9999)
        async with self.db_session_factory() as session:
            try:
                new_permission = Permission(
                    id=permission_id,
                    title=title,
                    slug=slug,
                    description=description,
                    active=active,
                    created_at=created_at,
                    context=context
                )
                session.add(new_permission)
                await session.commit()
                await session.refresh(new_permission)
                return new_permission
            except Exception as e:
                print(f"Error creating permission: {e}")
                await session.rollback()
                return None
                   
    async def get_all_permissions(self):
        async with self.db_session_factory() as session:
            try:
                all_permission = await session.execute(select(Permission))
                return all_permission.scalars().all()
            except Exception as e:
                print(f"Error fetching permissions: {e}")
                return None

    async def get_permission_by_id(self, permission_id):
        async with self.db_session_factory() as session:
            try:
                permission_id_query = await session.execute(select(Permission).filter_by(id=permission_id))
                return permission_id_query.scalar_one_or_none()
            except Exception as e:
                print(f"Error fetching permission by id: {e}")
                return None                