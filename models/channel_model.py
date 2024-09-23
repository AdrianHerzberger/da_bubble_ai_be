from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from storage.db_instance import db 
from .channel_user_association_model import ChannelUserAssociation

class Channel(db.Model):
    __tablename__ = 'channels'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    channel_name = db.Column(db.String(50), nullable=False)
    channel_description = db.Column(db.String(100), nullable=False)
    channel_color = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    
    user_associations = relationship('ChannelUserAssociation', back_populates='channel')
    users = relationship('User', secondary='channel_user_association', back_populates='channels', viewonly=True)
    
    def __repr__(self):
        return f'<Channel created with {self.channel_name}>'