from __future__ import annotations

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from project.database import BaseModel


class Accommodation(BaseModel):
    __tablename__ = "accommodation"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    website = Column(String, nullable=True)
    google_maps_place_id = Column(String, nullable=False)

    rooms = relationship("Room", backref="accommodation", uselist=True)

    @property
    def n_rooms(self) -> int:
        # TODO: Have to ignore type until relationship issues are fixed
        #       https://github.com/dropbox/sqlalchemy-stubs/issues/107
        return len(self.rooms)  # type: ignore


class Room(BaseModel):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    accomodation_id = Column(Integer, ForeignKey("accommodation.id"), nullable=False, index=True)
    name = Column(String, nullable=True)
    price_per_night = Column(Float, nullable=False)
