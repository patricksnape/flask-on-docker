from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from functools import cached_property
from typing import List, Optional, Tuple, Union, cast

from flask import Request
from flask_wtf import FlaskForm
from sqlalchemy.orm.session import Session

from project import BaseModel, RSVPForm
from project.database.booking import Booking
from project.database.party import Guest, Party
from project.rsvp.forms import RSVPFormWithAccommodation


@dataclass
class RSVPState:
    party: Party
    booking: Optional[Booking]

    @classmethod
    def init_from_party_id(cls, party_id: int, session: Session) -> RSVPState:
        party = Party.get_preload(party_id, session)
        booking = session.query(Booking).get(party_id)

        return cls(party=party, booking=booking)

    def update_db_with_form_data(self, form: Union[RSVPForm, RSVPFormWithAccommodation], session: Session) -> None:
        to_update: List[BaseModel] = []

        any_attending = False
        guests_attending = form.guests_attending.data
        for guest in self.guests:
            # The "in" is a linear search but the number of guests is always < 4
            is_attending = guest.id in guests_attending and form.attending.data
            any_attending |= is_attending
            guest.attending = is_attending
            to_update.append(guest)

        if self.booking is not None and any_attending:
            self.booking.check_in = form.accommodation_check_in.data
            self.booking.check_out = form.accommodation_check_out.data
            self.booking.accepted = form.accommodation_price_accepted.data
            to_update.append(self.booking)

        session.add_all(to_update)
        session.commit()

    @cached_property
    def attending(self) -> Optional[bool]:
        attending = None
        for g in self.guests:
            # The default is to assume guests are attending unless explicitly marked False
            if g.attending is not None:
                if attending is None:  # Have to convert None to boolean
                    attending = g.attending
                attending |= g.attending

        return attending

    @property
    def guests(self) -> List[Guest]:
        return cast(List[Guest], self.party.guests)

    @property
    def accommodation_check_in(self) -> Optional[date]:
        return self.booking.check_in if self.booking is not None else None

    @property
    def accommodation_check_out(self) -> Optional[date]:
        return self.booking.check_out if self.booking is not None else None

    @property
    def accommodation_price_accepted(self) -> bool:
        if self.booking is None:
            return False
        elif self.booking.accepted is None:
            # Default is True if the RSVP is uncompleted
            return True
        else:
            return self.booking.accepted

    @cached_property
    def guest_choices(self) -> List[Tuple[int, str]]:
        return [(g.id, g.full_name) for g in self.guests]

    @cached_property
    def attending_guest_ids(self) -> List[int]:
        # The default is to assume guests are attending unless explicitly marked False
        return [g.id for g in self.guests if g.attending is not False]

    @property
    def guests_attending(self) -> List[int]:
        # This only exists because the wtforms logic means the attributes are matched exactly
        # So it's a bad name but it has to match the name below
        return self.attending_guest_ids

    def build_form(self, request: Optional[Request] = None) -> FlaskForm:
        # This will build the form correctly (including setting up any dynamic fields)
        # as well as ensuring the correct form is created
        form = RSVPForm() if self.booking is None else RSVPFormWithAccommodation()
        form.guests_attending.choices = self.guest_choices
        form.process(formdata=request.form or None if request else None, obj=self)

        return form
