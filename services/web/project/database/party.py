from __future__ import annotations

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session, joinedload, relationship

from project.database import BaseModel


class Party(BaseModel):
    __tablename__ = "party"

    id = Column(Integer, primary_key=True)
    guest_code = Column(String(6), nullable=False, unique=True, index=True)

    guests = relationship("Guest", backref="party", uselist=True)

    @property
    def has_rsvpd(self):
        return all(g.attending is not None for g in self.guests)

    @property
    def is_attending(self):
        return any(g.attending is True for g in self.guests)

    @classmethod
    def get_preload(cls, party_id: int, session: Session) -> Party:
        """
        Get the party for the given ID and preload the guests associated with the party to avoid extra calls to the
        database (via SQL joins).

        Args:
            party_id : The primary key
            session : The session to use for querying the database

        Returns:
            The party object associated with the given primary key whereby the
                party.guests

            attribute is preloaded for faster access.
        """
        return session.query(cls).options(joinedload(Party.guests)).get(party_id)


class Guest(BaseModel):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True)
    party_id = Column(Integer, ForeignKey("party.id"), nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    attending = Column(Boolean, nullable=True)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".title()
