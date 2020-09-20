from flask import current_app
from flask_user.forms import RegisterForm
from flask_user.translation_utils import lazy_gettext as _
from wtforms import StringField, ValidationError, validators

from project.database.party import Party


def guest_code_exists(form, field) -> None:
    user_manager = current_app.user_manager
    session = user_manager.db.session
    guest_code = field.data
    if Party.get_by_guest_code(guest_code, session) is None:
        raise ValidationError(_("Unknown Guest Code"))


class GuestCodeRegisterForm(RegisterForm):
    guest_code = StringField(
        "Guest Code",
        validators=[
            validators.DataRequired(_("Guest Code Required")),
            validators.Length(min=6, max=6, message=_("Guest Code must be exactly 6 characters")),
            guest_code_exists,
        ],
    )
