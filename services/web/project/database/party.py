from __future__ import annotations

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from project.database import BaseModel


class Party(BaseModel):
    __tablename__ = "party"

    id = Column(Integer, primary_key=True)
    guest_code = Column(String(6), nullable=False, unique=True, index=True)

    guests = relationship("Guest", backref="party", uselist=True)


class Guest(BaseModel):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True)
    party_id = Column(Integer, ForeignKey("party.id"), nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
