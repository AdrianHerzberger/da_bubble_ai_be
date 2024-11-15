import asyncio
from ..session_management.create_async_engine import AsyncSessionLocal, Base
from ..models.role_model import Role
from ..repository_manager.role_data_manager_interface import RoleDataManagerInterface
from sqlalchemy.future import select
import datetime
import random

class RoleDataManager(RoleDataManagerInterface):
    def __init__(self):
        self.db_session_factory = AsyncSessionLocal
        
    async def create_role(self, title, slug, description, active, context):
        created_at = datetime.datetime.utcnow()
        role_id = random.randint(100, 9999) 
        async with self.db_session_factory() as session:
            try:
                new_role = Role(
                    id=role_id,
                    title=title,
                    slug=slug,
                    description=description,
                    active=active,
                    created_at=created_at,
                    context=context
                )
                session.add(new_role)
                await session.commit()
                await session.refresh(new_role)
                return new_role
            except Exception as e:
                print(f"Error creating role: {e}")
                await session.rollback()
                return None
                      
    async def get_role_by_id(self, role_id):
        async with self.db_session_factory() as session:
            try:
                role_id_query = await session.execute(select(Role).filter_by(id=role_id))
                return role_id_query.scalar_one_or_none()
            except Exception as e:
                print(f"Error fetching role id : {e}")
                return None