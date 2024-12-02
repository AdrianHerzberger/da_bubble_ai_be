import asyncio
from ..models.direct_message_model import DirectMessage
from ..storage_manager.direct_message_data_manager_interface import DirectMessageDataManagerInterface
from ..instances.create_async_engine import AsyncSessionLocal
from ..configuartions.mapping_direct_message_indexs import mapping_direct_message_indexs
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
import datetime


class DirectMessageDataManager(DirectMessageDataManagerInterface):
    def __init__(self):
        self.db_session_factory = AsyncSessionLocal
         
    async def create_direct_message(self, sender_id, receiver_id, content):
        timestamp = datetime.datetime.utcnow()
        
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

    async def delete_direct_message(self, direct_message_id: str) -> bool:
        async with self.db_session_factory() as session:
            try:
                message_id_to_delete = await session.execute(
                    delete(DirectMessage)
                    .where(DirectMessage.id == direct_message_id)
                )

                if message_id_to_delete.rowcount == 0:
                    return False

                await session.commit()
                return True
            except Exception as e:
                print(f"Error deleting direct message: {e}")
                return None           

    async def update_direct_message(self, direct_message_id: str, message_content_update: str) -> bool:
        async with self.db_session_factory() as session:
            try:
                message_id_to_update = await session.execute(
                    update(DirectMessage)
                    .where(DirectMessage.id == direct_message_id)
                    .values(content=message_content_update)
                )

                if message_id_to_update.rowcount == 0:
                    return False

                await session.commit()
                return True
            except Exception as e:
                print(f"Error updating direct message: {e}")
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