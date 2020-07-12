from __future__ import annotations

from typing import Optional

from flask_user import UserMixin
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relationship, Session

from project.database import BaseModel


class User(BaseModel, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    active = Column("is_active", Boolean, nullable=False, server_default="1")

    email = Column(String, nullable=False, unique=True, index=True)
    email_confirmed_at = Column(DateTime)
    password = Column(String, nullable=False)

    party_id = Column(Integer, ForeignKey("party.id"), index=True)

    roles = relationship("Role", secondary="user_roles")

    @classmethod
    def get_by_guest_code(cls, guest_code: str, session: Session) -> Optional[User]:
        from project.database.party import Party

        return (
            session.query(User)
            .join(Party, Party.id == User.party_id)
            .filter(Party.guest_code == guest_code.upper())
            .one_or_none()
        )


class Role(BaseModel):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class UserRoles(BaseModel):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), index=True)
