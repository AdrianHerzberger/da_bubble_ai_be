import uuid 
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
import datetime
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import relationship
from ..instances.db_instance import db 
from .channel_user_association_model import ChannelUserAssociation
from .channel_message_model import ChannelMessage

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_email = db.Column(db.String(200), nullable=False)  
    user_name = db.Column(db.String(100), nullable=False) 
    user_password = db.Column(db.String(255), nullable=False) 
    user_profile_picture_url = db.Column(db.String(255), nullable=True)
    
    last_login_date = db.Column(DateTime, nullable=True)
    create_date = db.Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    password_expire_date = db.Column(DateTime, nullable=True)
    is_locked = db.Column(Boolean, default=False, nullable=False)
    status = db.Column(String(50), nullable=False, default="active")
    
    channel_associations = relationship('ChannelUserAssociation', back_populates='user')
    channels = relationship('Channel', secondary='channel_user_association', back_populates='users', viewonly=True)
    channel_messages = relationship('ChannelMessage', back_populates='sender')

    def __repr__(self):
        return f'<User created with {self.user_name} {self.user_password}>'
