from __future__ import annotations

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer
from sqlalchemy.orm import Session, lazyload, relationship

from project.database import BaseModel
from project.database.accommodation import Room


class Booking(BaseModel):
    __tablename__ = "booking"

    party_id = Column(Integer, ForeignKey("party.id"), primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False, unique=True, index=True)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    accepted = Column(Boolean, nullable=True)

    room = relationship("Room")

    @property
    def n_nights(self) -> int:
        return (self.check_out - self.check_in).days

    @property
    def total_cost(self) -> float:
        return self.n_nights * self.room.price_per_night

    @classmethod
    def get_preload(cls, party_id: int, session: Session) -> Booking:
        """
        Get the booking for the given party ID an preload the room and accommodation associated
        with the booking to avoid extra calls to the database (via SQL joins).

        Args:
            party_id : The primary key
            session : The session to use for querying the database

        Returns:
            The booking object associated with the given primary key whereby the
                booking.room
                booking.room.accommodation

            attributes are preloaded for faster access.
        """
        return session.query(Booking).options(lazyload(Booking.room).joinedload(Room.accommodation)).get(party_id)
