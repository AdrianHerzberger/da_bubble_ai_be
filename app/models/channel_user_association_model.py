import uuid
from sqlalchemy import Integer, ForeignKey, Column
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import relationship
from ..instances.create_async_engine import Base  

class ChannelUserAssociation(Base):
    __tablename__ = 'channel_user_association'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    channel_id = Column(UUID(as_uuid=True), ForeignKey('channels.id'), primary_key=True)
    
    user = relationship('User', back_populates='channel_associations')
    channel = relationship('Channel', back_populates='user_associations')
