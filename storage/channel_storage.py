from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .db_instance import db 

class Channel(db.Model):
    __tablename__ = 'channels'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    channel_name = db.Column(db.String(50), nullable=False)
    channel_description = db.Column(db.String(100), nullable=False)
    channel_color = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.String, ForeignKey('users.id'), nullable=False)
    
    #user = relationship('User', back_populates='channels')
    
    def __repr__(self):
        return f'<Channel created with {self.channel_name}>'
