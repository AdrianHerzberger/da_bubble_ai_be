from sqlalchemy import BigInteger, Boolean, Integer, ForeignKey, Column, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID 
from ..session_management.create_async_engine import Base 


class RolePermission(Base):
    __tablename__ = "role_permission"
    
    role_id = Column(BigInteger, ForeignKey('roles.id'), primary_key=True)
    permission_id = Column(BigInteger, ForeignKey('permissions.id'), primary_key=True)
    
    roles = relationship('Role', back_populates='user_roles')
    permissions = relationship('Permission', back_populates='user_permission')
    