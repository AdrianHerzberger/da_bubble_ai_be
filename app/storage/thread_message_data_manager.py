import asyncio
from ..instances.create_async_engine import AsyncSessionLocal
from ..models.thread_message_model import ThreadMessage
from ..storage_manager.thread_data_manager_interface import ThreadMessageDataManagerInterface
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
import datetime
import random


class ThreadMessageDataManager(ThreadMessageDataManagerInterface):
    def __init__(self):
        self.db_session_factory = AsyncSessionLocal
           
    async def create_thread(self, thread_type, channel_message_id, direct_message_id, content, thread_suggestion):
        
        if not (channel_message_id or direct_message_id):
            raise ValueError("Either channel_message_id or direct_message_id must be provided.")
        if channel_message_id and direct_message_id:
            raise ValueError("Only one of channel_message_id or direct_message_id can be provided.")
        if thread_type == "channel" and not channel_message_id:
            raise ValueError("channel_message_id is required for a 'channel' thread.")
        if thread_type == "direct" and not direct_message_id:
            raise ValueError("direct_message_id is required for a 'direct' thread.")
        if thread_type not in ["channel", "direct"]:
            raise ValueError("Invalid thread_type. Must be 'channel' or 'direct'.")
        
        created_at = datetime.datetime.utcnow()
        
        async with self.db_session_factory() as session:
            try:
                new_thread = ThreadMessage(
                    thread_type=thread_type,
                    channel_message_id=channel_message_id,
                    direct_message_id=direct_message_id,
                    thread_suggestion=thread_suggestion,
                    content=content,
                    created_at=created_at
                )
                print(f"newly created thread message: {new_thread}")
                session.add(new_thread)
                await session.commit()
                await session.refresh(new_thread)
                return new_thread
            except Exception as e:
                print(f"Error creating message: {e}")
                await session.rollback()
                return None
                     
    async def get_thread_messages_channel_id(self, channel_message_id):
        async with self.db_session_factory() as session:
            try:
                channel_message_id_query = await session.execute(select(ThreadMessage).filter_by(channel_message_id=channel_message_id))
                message = channel_message_id_query.scalar_one_or_none()
                return message
            except Exception as e:
                print(f"Error fetching thread message for channel: {e}")
                return None
            
    async def get_thread_messages_direct_id(self, direct_message_id):
        async with self.db_session_factory() as session:
            try:
                direct_message_id_query = await session.execute(select(ThreadMessage).filter_by(direct_message_id=direct_message_id))
                messages = direct_message_id_query.scalar_one_or_none()
                return messages
            except Exception as e:
                print(f"Error fetching thread message from direct chat: {e}")
                return None
            
    async def get_all_thread_messages(self):
        async with self.db_session_factory() as session:
            try:
                all_thread_messages = await session.execute(select(ThreadMessage))
                return all_thread_messages.scalars().all()
            except Exception as e:
                print(f"Error fetching all thread messages: {e}")
                return None
        
            