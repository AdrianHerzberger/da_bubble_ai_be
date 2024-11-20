import asyncio
from ..instances.create_async_engine import AsyncSessionLocal
from ..models.channel_model import Channel
from ..repository_manager.channel_data_manager_interface import ChannelDataManagerInterface
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
import datetime
import random

class ChannelDataManager(ChannelDataManagerInterface):
    def __init__(self):
        self.db_session_factory = AsyncSessionLocal

    async def create_channel(self, channel_name, channel_description, user_id):
        channel_color = "%06x" % random.randint(0, 0xFFFFFF)
        create_date = datetime.datetime.utcnow()
        
        async with self.db_session_factory() as session:
            try:
                new_channel = Channel(
                    channel_name=channel_name,
                    channel_description=channel_description,
                    channel_color=channel_color,
                    create_date=create_date,
                    user_id=user_id
                )
                session.add(new_channel)
                await session.commit()
                await session.refresh(new_channel)
                return new_channel
            except Exception as e:
                print(f"Error creating channel: {e}")
                session.rollback()
                return None

    async def get_channel_by_id(self, channel_id):
        async with self.db_session_factory() as session:
            try:
                channel_id_query = await session.execute(select(Channel).filter_by(id=channel_id))
                return channel_id_query.scalar_one_or_none()
            except Exception as e:
                print(f"Error fetching channel: {e}")
                return None
        
    async def get_all_channels(self):
        async with self.db_session_factory() as session:
            try:
                all_channels = await session.execute(select(Channel))
                return all_channels.scalars().all()
            except Exception as e:
                print(f"Error fetching all channels: {e}")
                return None