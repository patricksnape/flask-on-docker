from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from project import BaseModel
from project.database.booking import Booking
from project.database.party import Party

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from project.rsvp.rsvp import FrozenRSVPState


# This is my poor man's version control - explicitly keep track of the changes to the RSVPs so we can act on them
# as they happen. However, the current state of the database should always be considered the canonical state and
# this table is basically just used to review changes.
class RSVPChange(BaseModel):
    __tablename__ = "rsvp_changes"

    id = Column(Integer, primary_key=True)
    party_id = Column(Integer, ForeignKey("party.id"), index=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    guest_ids_before = Column(ARRAY(Integer), nullable=True)
    guest_ids_after = Column(ARRAY(Integer), nullable=True)
    check_in_before = Column(Date, nullable=True)
    check_in_after = Column(Date, nullable=True)
    check_out_before = Column(Date, nullable=True)
    check_out_after = Column(Date, nullable=True)
    accepted_before = Column(Boolean, nullable=True)
    accepted_after = Column(Boolean, nullable=True)
    reviewed = Column(Boolean, nullable=False)

    party = relationship("Party")
    booking = relationship(
        "Booking", secondary="party", primaryjoin=Party.id == party_id, secondaryjoin=Booking.party_id == Party.id,
    )

    @property
    def rsvp_declined(self):
        return not self.guest_ids_after

    @classmethod
    def insert(cls, party_id: int, old: FrozenRSVPState, new: FrozenRSVPState, session: Session) -> RSVPChange:

        state = cls(
            party_id=party_id,
            guest_ids_before=old.guest_ids,
            guest_ids_after=new.guest_ids,
            check_in_before=old.check_in,
            check_in_after=new.check_in,
            check_out_before=old.check_out,
            check_out_after=new.check_out,
            accepted_before=old.accepted,
            accepted_after=new.accepted,
            reviewed=False,
        )
        # Get the most recent change if there is one
        most_recent_state = (
            session.query(cls).filter_by(party_id=party_id).order_by(cls.created_at.desc()).limit(1).one_or_none()
        )
        if state.different(most_recent_state):
            session.add(state)
            session.commit()

        return state

    def different(self, other: Optional[RSVPChange]) -> bool:
        if other is None:
            return True

        columns = {i.name: (getattr(self, i.name), getattr(other, i.name)) for i in self.__table__.columns}
        for name, (this_value, other_value) in columns.items():
            if name not in ("id", "created_at", "reviewed") and this_value != other_value:
                return True

        return False