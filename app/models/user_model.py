import uuid 
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
import datetime
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import relationship
from ..session_management.create_async_engine import Base 
from .channel_user_association_model import ChannelUserAssociation
from .channel_message_model import ChannelMessage 

class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_email = Column(String(200), nullable=False)  
    user_name = Column(String(100), nullable=False) 
    user_password = Column(String(255), nullable=False) 
    user_profile_picture_url = Column(String(255), nullable=True)
    
    last_login_date = Column(DateTime, nullable=True)
    create_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    password_expire_date = Column(DateTime, nullable=True)
    is_locked = Column(Boolean, default=False, nullable=False)
    status = Column(String(50), nullable=False, default="active")
    
    channel_associations = relationship('ChannelUserAssociation', back_populates='user')
    channels = relationship('Channel', secondary='channel_user_association', back_populates='users', viewonly=True)
    channel_messages = relationship('ChannelMessage', back_populates='sender')

    def __repr__(self):
        return f'<User created with {self.user_name} {self.user_password}>'
