import uuid
from sqlalchemy import Integer, ForeignKey, Column
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import relationship
from ..instances.db_instance import db 

class ChannelUserAssociation(db.Model):
    __tablename__ = 'channel_user_association'
    
    user_id = db.Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    channel_id = db.Column(UUID(as_uuid=True), ForeignKey('channels.id'), primary_key=True)
    
    user = relationship('User', back_populates='channel_associations')
    channel = relationship('Channel', back_populates='user_associations')
