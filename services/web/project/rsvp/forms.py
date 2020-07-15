from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from project.translations.utils import lazy_gettext as _


class RSVPForm(FlaskForm):
    attending = RadioField(_("Attending"), coerce=int, choices=[(1, _("Yes")), (0, _("No"))])

    submit = SubmitField(_("Submit"))
