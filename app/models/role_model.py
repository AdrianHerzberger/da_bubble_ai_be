import uuid
from sqlalchemy import BigInteger, Boolean, String, Integer, ForeignKey, Column, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID 
from ..session_management.create_async_engine import Base 
import datetime

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(BigInteger, primary_key=True)
    title = Column(String(75), nullable=False)
    slug = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    active = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    context = Column(Text, nullable=False)
    
    users = relationship('User', back_populates='role')
    user_roles = relationship('RolePermission', back_populates='roles')