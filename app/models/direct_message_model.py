import uuid
from sqlalchemy import Integer, ForeignKey, Column, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import relationship
from ..instances.create_async_engine import Base 
import datetime

class DirectMessage(Base):
    __tablename__ = 'direct_messages'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    sender = relationship('User', foreign_keys=[sender_id], back_populates='sent_messages')
    receiver = relationship('User', foreign_keys=[receiver_id], back_populates='received_messages')

    
