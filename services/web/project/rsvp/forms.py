from __future__ import annotations

from datetime import date, timedelta

from flask_wtf import FlaskForm
from wtforms import BooleanField, RadioField, SelectMultipleField, SubmitField, validators, widgets
from wtforms_components import DateField, DateRange

from project.config import Config
from project.translations.utils import lazy_gettext as _


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


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
            DateRange(min=Config.BOOKING_MIN_DATE, max=Config.WEDDING_DATETIME.date()),
        ],
    )
    accommodation_check_out = DateField(
        _("Check-Out Date"),
        format="%Y-%m-%d",
        validators=[
            validators.DataRequired(message=_("You must provide a check-out date")),
            DateRange(min=Config.WEDDING_DATETIME.date() + timedelta(days=1), max=Config.BOOKING_MAX_DATE),
        ],
    )
    accommodation_price_accepted = BooleanField(_("I accept the price per night of "), default=True)

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
