import uuid
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import relationship
from ..session_management.create_async_engine import Base 
import datetime


class ChannelMessage(Base):
    __tablename__ = 'channel_messages'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id = Column(UUID(as_uuid=True), ForeignKey('channels.id'), nullable=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow) 
    
    sender = relationship('User', back_populates='channel_messages')
    channel = relationship('Channel', back_populates='messages')
    
        
    
     