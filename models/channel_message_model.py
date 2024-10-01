from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from storage.db_instance import db
import datetime


class ChannelMessage(db.Model):
    __tablename__ = 'channel_messages'

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow) 
    
    sender = relationship('User', back_populates='channel_messages')
    channel = relationship('Channel', back_populates='messages')
    
        
    
     