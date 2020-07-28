from __future__ import annotations

from typing import Optional

from flask import current_app
from flask_user import UserMixin
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship

from project.database import BaseModel


class User(BaseModel, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    active = Column("is_active", Boolean, nullable=False, server_default="1")

    email = Column(String, nullable=False, unique=True, index=True)
    email_confirmed_at = Column(DateTime)
    password = Column(String, nullable=False)

    party_id = Column(Integer, ForeignKey("party.id"), index=True, nullable=True)

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

    @classmethod
    def get_by_party_id(cls, party_id: int, session: Session) -> Optional[User]:
        return session.query(User).filter_by(party_id=party_id).one_or_none()

    @classmethod
    def get_user_by_token(cls, token, expiration_in_seconds=None):
        # I had to override this due to a bug in the implementation when no
        # user exists
        user_manager = current_app.user_manager
        data_items = user_manager.verify_token(token, expiration_in_seconds)

        token_is_valid = False
        user = None
        if data_items:
            user_id, password_ends_with = data_items
            user = user_manager.db_manager.get_user_by_id(user_id)
            if user is not None:  # FIX HERE
                user_password = "" if user_manager.USER_ENABLE_AUTH0 else user.password[-8:]
                token_is_valid = user and user_password == password_ends_with

        return user if token_is_valid else None


class Role(BaseModel):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class UserRoles(BaseModel):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), index=True)
