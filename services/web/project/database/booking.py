from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from project.database import BaseModel

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from project.database.accomodation import Room


class Booking(BaseModel):
    __tablename__ = "booking"

    party_id = Column(Integer, ForeignKey("party.id"), primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False, unique=True, index=True)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)

    room = relationship("Room")

    @property
    def n_nights(self) -> int:
        return (self.check_out - self.check_in).days

    @property
    def total_cost(self) -> float:
        return self.n_nights * self.room.price_per_night
