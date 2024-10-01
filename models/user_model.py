from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from storage.db_instance import db
from .channel_user_association_model import ChannelUserAssociation
from .channel_message_model import ChannelMessage

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    user_email = db.Column(db.String(200), nullable=False)  
    user_name = db.Column(db.String(100), nullable=False) 
    user_password = db.Column(db.String(255), nullable=False) 
    user_profile_picture_url = db.Column(db.String(255), nullable=True)
    
    channel_associations = relationship('ChannelUserAssociation', back_populates='user')
    channels = relationship('Channel', secondary='channel_user_association', back_populates='users', viewonly=True)
    channel_messages = relationship('ChannelMessage', back_populates='sender')

    def __repr__(self):
        return f'<User created with {self.user_name} {self.user_password}>'
