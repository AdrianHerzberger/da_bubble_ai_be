from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .db_instance import db 

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(200), nullable=False)  
    user_name = db.Column(db.String(100), nullable=False) 
    user_password = db.Column(db.String(255), nullable=False) 
    user_profile_picture_url = db.Column(db.String(255), nullable=True)
    
    channels = relationship('Channel', back_populates='user')

    def __repr__(self):
        return f'<User created with {self.user_name} {self.user_password}>'
