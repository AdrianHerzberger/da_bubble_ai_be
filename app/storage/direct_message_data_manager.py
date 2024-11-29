import asyncio
from ..models.direct_message_model import DirectMessage
from ..storage_manager.direct_message_data_manager_interface import DirectMessageDataManagerInterface
from ..instances.create_async_engine import AsyncSessionLocal
from ..configuartions.mapping_direct_message_indexs import mapping_direct_message_indexs
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
import datetime


class DirectMessageDataManager(DirectMessageDataManagerInterface):
    def __init__(self):
        self.db_session_factory = AsyncSessionLocal
         
    async def create_direct_message(self, sender_id, receiver_id, content):
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        
        async with self.db_session_factory() as session:
            try:
                new_message = DirectMessage(
                    sender_id=sender_id,
                    receiver_id=receiver_id,
                    content=content,
                    timestamp=timestamp,
                )
                session.add(new_message)
                await session.commit()
                await session.refresh(new_message)
                await mapping_direct_message_indexs([new_message])
                return new_message          
            except Exception as e:
                print(f"Error creating message: {e}")
                await session.rollback()
                return None
            
    async def get_direct_messages_by_id(self, receiver_id, search_index=any):
        async with self.db_session_factory() as session:
            try:
                direct_message_id_query = await session.execute(select(DirectMessage).filter_by(receiver_id=receiver_id))
                messages = direct_message_id_query.scalars().all()
                if not search_index:
                    if messages:
                        await mapping_direct_message_indexs(messages)
                return messages
            except Exception as e:
                print(f"Error fetching direct message: {e}")
                return None
            
    async def get_all_direct_messages(self):
        async with self.db_session_factory() as session:
            try:
                all_direct_messages = await session.execute(select(DirectMessage))
                return all_direct_messages.scalars().all()
            except Exception as e:
                print(f"Error fetching direct messages: {e}")
                return None