import uuid
from sqlalchemy import BigInteger, Column, Integer, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import relationship
from ..session_management.create_async_engine import Base 

class Channel(Base):
    __tablename__ = 'channels'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_name = Column(String(50), nullable=False)
    channel_description = Column(String(100), nullable=False)
    channel_color = Column(String(50), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    user_associations = relationship('ChannelUserAssociation', back_populates='channel')
    users = relationship('User', secondary='channel_user_association', back_populates='channels', viewonly=True)
    messages = relationship('ChannelMessage', back_populates='channel')
    
    def __repr__(self):
        return f'<Channel created with {self.channel_name}>'
