from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from functools import cached_property
from typing import List, Optional, TYPE_CHECKING, Tuple, cast

from flask_wtf import FlaskForm
from wtforms import RadioField, SelectMultipleField, SubmitField, validators, widgets
from wtforms_components import DateField, DateRange

from project.config import Config
from project.database import BaseModel
from project.database.booking import Booking
from project.database.party import Guest, Party
from project.translations.utils import lazy_gettext as _

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from flask import Request


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


@dataclass
class RSVPState:
    party: Party
    booking: Optional[Booking]

    @classmethod
    def init_from_party_id(cls, party_id: int, session: Session) -> RSVPState:
        party = session.query(Party).get(party_id)
        booking = session.query(Booking).get(party_id)

        return cls(party=party, booking=booking)

    def update_db_with_form_data(self, form: RSVPForm, session: Session) -> None:
        to_update: List[BaseModel] = []

        guests_attending = form.guests_attending.data
        for guest in self.guests:
            # The "in" is a linear search but the number of guests is always < 4
            guest.attending = guest.id in guests_attending and form.attending.data
            to_update.append(guest)

        if self.booking is not None:
            self.booking.check_in = form.accommodation_check_in.data
            self.booking.check_out = form.accommodation_check_out.data
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


class RSVPForm(FlaskForm):
    attending = RadioField(
        _("Attending"),
        coerce=int,
        choices=[(1, _("Yes")), (0, _("No"))],
        validators=[validators.InputRequired(_("Please select whether you are able to attend or not"))],
    )
    guests_attending = MultiCheckboxField(_("Guests Attending"), coerce=int)

    submit = SubmitField(_("Submit"))

    @property
    def n_guests_attending(self) -> int:
        return len(self.guests_attending.data)

    @property
    def attending_selected(self) -> bool:
        return self.attending.data

    def validate(self, extra_validators=None):
        success = super().validate(extra_validators)
        if self.attending_selected and self.n_guests_attending == 0:
            self.guests_attending.errors.append(_("Please select at least one guest as attending or select 'No' above"))
            success = False

        return success


class RSVPFormWithAccommodation(RSVPForm):
    accommodation_check_in = DateField(
        _("Check-In Date"),
        format="%Y-%m-%d",
        validators=[
            validators.DataRequired(message=_("You must provide a check-in date")),
            DateRange(min=Config.BOOKING_MIN_DATE, max=Config.WEDDING_DATE),
        ],
    )
    accommodation_check_out = DateField(
        _("Check-Out Date"),
        format="%Y-%m-%d",
        validators=[
            validators.DataRequired(message=_("You must provide a check-out date")),
            DateRange(min=Config.WEDDING_DATE + timedelta(days=1), max=Config.BOOKING_MAX_DATE),
        ],
    )

    @property
    def check_out_date(self) -> date:
        return self.accommodation_check_out.data

    @property
    def check_in_date(self) -> date:
        return self.accommodation_check_in.data

    def validate(self, extra_validators=None):
        success = super().validate(extra_validators)

        if self.check_out_date <= self.check_in_date:
            self.accommodation_check_out.errors.append(_("Please ensure the check-out date is after the check-in date"))
            success = False

        return success
