from __future__ import annotations

from dataclasses import dataclass, fields
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, and_, func, select
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from project import BaseModel
from project.database.booking import Booking
from project.database.party import Guest, Party

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
    # Note using an Array to store foreign keys is a naughty anti-pattern to avoid creating yet another table to store
    # the changes per user
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

    __before_guests_selectable = select(
        [func.unnest(guest_ids_before).label("guest_id"), id.label("rsvp_change_id")]
    ).alias("guest_ids")

    guests_before = relationship(
        Guest,
        secondary=__before_guests_selectable,
        primaryjoin=and_(
            Guest.id == __before_guests_selectable.c.guest_id, __before_guests_selectable.c.rsvp_change_id == id
        ),
        secondaryjoin=__before_guests_selectable.c.rsvp_change_id == id,
        order_by=__before_guests_selectable.c.rsvp_change_id,
        uselist=True,
        viewonly=True,
    )

    __after_guests_selectable = select(
        [func.unnest(guest_ids_after).label("guest_id"), id.label("rsvp_change_id")]
    ).alias("guest_ids")

    guests_after = relationship(
        Guest,
        secondary=__after_guests_selectable,
        primaryjoin=and_(
            Guest.id == __after_guests_selectable.c.guest_id, __after_guests_selectable.c.rsvp_change_id == id
        ),
        secondaryjoin=__after_guests_selectable.c.rsvp_change_id == id,
        order_by=__after_guests_selectable.c.rsvp_change_id,
        uselist=True,
        viewonly=True,
    )

    # Private class for the change-set
    @dataclass(frozen=True)
    class ChangeSet:
        guests: Optional[List[str]]
        check_in: Optional[str]
        check_out: Optional[str]
        accepted: Optional[str]

        @property
        def has_accommodation_change(self):
            return self.check_in is not None or self.check_out is not None or self.accepted is not None

        def is_empty(self) -> bool:
            return all(getattr(self, x.name) is None for x in fields(self))

    @property
    def rsvp_declined(self):
        return not self.guest_ids_after

    @classmethod
    def get_all_unreviewed_party_ids(cls, session: Session) -> List[int]:
        return [
            row[0]
            for row in session.query(cls.party_id.distinct()).filter_by(reviewed=False).order_by(cls.party_id).all()
        ]

    @classmethod
    def get_all_for_party_id(cls, party_id: int, session: Session) -> List[RSVPChange]:
        return session.query(cls).filter_by(party_id=party_id).order_by(cls.created_at.desc()).all()

    @classmethod
    def insert(cls, party_id: int, old: FrozenRSVPState, new: FrozenRSVPState, session: Session) -> RSVPChange:
        # Get the most recent change if there is one
        most_recent_state = (
            session.query(cls).filter_by(party_id=party_id).order_by(cls.created_at.desc()).limit(1).one_or_none()
        )

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

        if state.different(most_recent_state):
            # If the state is actually completely the same then we can just mark it as reviewed. Note this only
            # happens for the first RSVP when the user doesn't change any values (and we can thus ignore needing
            # to review the changes)
            state.reviewed = state.is_empty()

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

    def is_empty(self) -> bool:
        return self.changes().is_empty()

    def changes(self) -> RSVPChange.ChangeSet:
        guests = None
        if self.guest_ids_before != self.guest_ids_after and None not in {self.guest_ids_before, self.guest_ids_after}:
            assert self.guest_ids_after is not None
            assert self.guest_ids_before is not None

            guests = []
            changed_ids = set(self.guest_ids_before).symmetric_difference(self.guest_ids_after)
            for guest in self.guests_before:
                if guest.id in changed_ids:
                    # They were in before, but not in after (so they now declined)
                    guests.append(f"{guest.full_name} is no longer attending")

            for guest in self.guests_after:
                if guest.id in changed_ids:
                    # They were not in before, but now are (so they now accepted)
                    guests.append(f"{guest.full_name} is now attending")

        accepted = None
        if self.accepted_before != self.accepted_after:
            if self.accepted_before:
                # Not equal so must now not be unaccepted
                accepted = "The accommodation price was unaccepted"
            else:
                accepted = "The accommodation price was accepted"

        check_in = None
        if self.check_in_before != self.check_in_after:
            check_in = f"Check-In changed from {self.check_in_before} to {self.check_in_after}"

        check_out = None
        if self.check_out_before != self.check_out_after:
            check_out = f" Check-out changed from {self.check_out_before} to {self.check_out_after:}"

        return RSVPChange.ChangeSet(guests=guests, check_in=check_in, check_out=check_out, accepted=accepted)
