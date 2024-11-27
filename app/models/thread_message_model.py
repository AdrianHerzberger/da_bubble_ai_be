import uuid
from sqlalchemy import ARRAY, Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import relationship
from ..instances.create_async_engine import Base 
import datetime


class ThreadMessage(Base):
    __tablename__ = 'thread_messages'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    thread_type = Column(String, nullable=False)  
    channel_message_id = Column(UUID(as_uuid=True), ForeignKey('channel_messages.id'), nullable=True)
    direct_message_id = Column(UUID(as_uuid=True), ForeignKey('direct_messages.id'), nullable=True)
    content = Column(Text, nullable=False)
    thread_suggestion = Column(ARRAY(String))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    channel_message = relationship('ChannelMessage', back_populates='thread')
    direct_message = relationship('DirectMessage', back_populates='thread')
    