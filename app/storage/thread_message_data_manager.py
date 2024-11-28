import asyncio
from ..instances.create_async_engine import AsyncSessionLocal
from ..models.thread_message_model import ThreadMessage
from ..storage_manager.thread_data_manager_interface import ThreadMessageDataManagerInterface
from ..exceptions.thread_excpetion_handler import validate_thread_inputs
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
import datetime
import random


class ThreadMessageDataManager(ThreadMessageDataManagerInterface):
    def __init__(self):
        self.db_session_factory = AsyncSessionLocal
           
    async def create_thread(self, thread_type, channel_message_id, direct_message_id, content, thread_suggestion):
        try:
            validate_thread_inputs(thread_type, channel_message_id, direct_message_id)
            
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
                    session.add(new_thread)
                    await session.commit()
                    await session.refresh(new_thread)
                    return new_thread
                except Exception as e:
                    print(f"Error creating message: {e}")
                    await session.rollback()
                    return None
        except ValueError as ve:
            print(f"Validation error: {ve}")
            return None
                     
    async def get_thread_messages_channel_id(self, channel_message_id):
        async with self.db_session_factory() as session:
            try:
                channel_message_id_query = await session.execute(select(ThreadMessage).filter_by(channel_message_id=channel_message_id))
                message = channel_message_id_query.scalars().all()
                return message
            except Exception as e:
                print(f"Error fetching thread message for channel: {e}")
                return None
            
    async def get_thread_messages_direct_id(self, direct_message_id):
        async with self.db_session_factory() as session:
            try:
                direct_message_id_query = await session.execute(select(ThreadMessage).filter_by(direct_message_id=direct_message_id))
                messages = direct_message_id_query.scalars().all()
                return messages
            except Exception as e:
                print(f"Error fetching thread message from direct chat: {e}")
                return None
            
        
            