from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, validators, SelectMultipleField, widgets
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

    accommodation_check_in = DateField(
        _("Check In Date"),
        format="%Y-%m-%d",
        validators=[
            validators.DataRequired(message=_("You must provide a check-in date")),
            DateRange(min=Config.BOOKING_MIN_DATE, max=Config.WEDDING_DATE),
        ],
    )

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
