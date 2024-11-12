import uuid
from sqlalchemy import BigInteger, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import relationship
from ..session_management.create_async_engine import Base 
import datetime

class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_email = Column(String(200), nullable=False)  
    user_name = Column(String(100), nullable=False) 
    user_password = Column(String(255), nullable=False) 
    user_profile_picture_url = Column(String(255), nullable=True)
    
    role_id = Column(BigInteger, ForeignKey('roles.id'), nullable=True)
    
    last_login_date = Column(DateTime, nullable=True)
    create_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    password_expire_date = Column(DateTime, nullable=True)
    is_locked = Column(Boolean, default=False, nullable=False)
    status = Column(String(50), nullable=False, default="active")
    
    role = relationship('Role', back_populates='users')
    
    channel_associations = relationship('ChannelUserAssociation', back_populates='user')
    channels = relationship('Channel', secondary='channel_user_association', back_populates='users', viewonly=True)
    channel_messages = relationship('ChannelMessage', back_populates='sender')
    
    sent_messages = relationship('DirectMessage', foreign_keys='DirectMessage.sender_id', back_populates='sender')
    received_messages = relationship('DirectMessage', foreign_keys='DirectMessage.receiver_id', back_populates='receiver')

    def __repr__(self):
        return f'<User created with {self.user_name} {self.user_password}>'
