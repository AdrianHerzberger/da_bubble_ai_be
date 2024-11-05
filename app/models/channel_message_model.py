import uuid
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import relationship
from ..instances.db_instance import db 
import datetime


class ChannelMessage(db.Model):
    __tablename__ = 'channel_messages'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow) 
    
    sender = relationship('User', back_populates='channel_messages')
    channel = relationship('Channel', back_populates='messages')
    
        
    
     