import asyncio
from ..instances.create_async_engine import AsyncSessionLocal
from ..models.channel_user_association_model import ChannelUserAssociation
from ..repository_manager.channel_user_association_data_manager_interface import ChannelUserAssociationDataManagerInterface
from ..models.user_model import User
from ..models.channel_model import Channel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select 
from sqlalchemy import and_ 


class ChannelUserAssociationManager(ChannelUserAssociationDataManagerInterface):
    def __init__(self):
        self.db_session_factory = AsyncSessionLocal

    async def create_channel_user_association(self, user_id, channel_id):
        async with self.db_session_factory() as session:
            try:
                
                existing_association_query = select(ChannelUserAssociation).filter(
                    and_(
                        ChannelUserAssociation.user_id == user_id,
                        ChannelUserAssociation.channel_id == channel_id
                    )
                )
                
                association_result = await session.execute(existing_association_query)
                existing_association = association_result.scalar_one_or_none()
                    
                if existing_association:
                    print(f"Association between user {user_id} and channel {channel_id} already exists.")
                    return  
                    
                new_channel_user_association = ChannelUserAssociation(
                    user_id=user_id,
                    channel_id=channel_id
                )
                session.add(new_channel_user_association)
                await session.commit()
                await session.refresh(new_channel_user_association)
                return new_channel_user_association
            except Exception as e:
                print(f"Error creating channel user association: {e}")
                await session.rollback()
                return False
            
    async def get_users_for_channel(self, channel_id):
        async with self.db_session_factory() as session:
            try:
                users_query = select(User).join(ChannelUserAssociation).filter(
                    ChannelUserAssociation.channel_id == channel_id
                )
                users_result = await session.execute(users_query)
                users = users_result.scalars().all() 
                print(f"User from the query : {users}") 

                users_for_channel = [
                    {
                        "user_id": user.id,
                        "username": user.user_name
                    }
                    for user in users
                ]
                return users_for_channel
            except Exception as e:
                print(f"Error getting users for channel {channel_id}: {e}")
                return None

    async def get_channels_for_user(self, user_id):
        async with self.db_session_factory() as session:
            try:
                channels_query = select(Channel).join(ChannelUserAssociation).filter(
                    ChannelUserAssociation.user_id == user_id
                )           
                channels_result = await session.execute(channels_query)
                channels = channels_result.scalars().all()
                
                channels_for_user = [
                    {
                        "channel_id": channel.id,
                        "channel_name": channel.channel_name,
                        "channel_description": channel.channel_description,
                        "channel_color": channel.channel_color
                    }
                    for channel in channels
                ]
                return channels_for_user               
            except Exception as e:
                print(f"Error getting user for channel {user_id}: {e}")
                return None    