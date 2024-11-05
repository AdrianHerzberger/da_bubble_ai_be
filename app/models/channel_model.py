import uuid
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import relationship
from ..instances.db_instance import db 
from .channel_user_association_model import ChannelUserAssociation
from .channel_message_model import ChannelMessage

class Channel(db.Model):
    __tablename__ = 'channels'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_name = db.Column(db.String(50), nullable=False)
    channel_description = db.Column(db.String(100), nullable=False)
    channel_color = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    
    user_associations = relationship('ChannelUserAssociation', back_populates='channel')
    users = relationship('User', secondary='channel_user_association', back_populates='channels', viewonly=True)
    messages = relationship('ChannelMessage', back_populates='channel')
    
    def __repr__(self):
        return f'<Channel created with {self.channel_name}>'
