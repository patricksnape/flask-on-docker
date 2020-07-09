from flask_user import UserMixin
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from project.database import BaseModel


class User(BaseModel, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    active = Column("is_active", Boolean, nullable=False, server_default="1")

    email = Column(String, nullable=False, unique=True)
    email_confirmed_at = Column(DateTime)
    password = Column(String, nullable=False)

    roles = relationship("Role", secondary="user_roles")


class Role(BaseModel):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class UserRoles(BaseModel):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"))
