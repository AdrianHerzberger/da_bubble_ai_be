from sqlalchemy import Integer, ForeignKey, Column
from sqlalchemy.orm import relationship
from storage.db_instance import db

class ChannelUserAssociation(db.Model):
    __tablename__ = 'channel_user_association'
    
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    
    user = relationship('User', back_populates='channel_associations')
    channel = relationship('Channel', back_populates='user_associations')
