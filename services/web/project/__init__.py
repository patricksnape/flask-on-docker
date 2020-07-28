from functools import wraps

from flask import Flask, abort, redirect, render_template, request
from flask_login import current_user
from flask_menu import Menu, register_menu
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, roles_accepted

from project.database import BaseModel
from project.database.rsvp import RSVPChange
from project.database.users import User
from project.jinja.autoescape import select_jinja_autoescape
from project.jinja.filters import custom_jinja_blueprint
from project.mail.mailgun import MailGunEmailAdapter
from project.rsvp.forms import RSVPForm
from project.rsvp.rsvp import RSVPState, RSVPStatistics
from project.user_flow.user_manager import WeddingUserManager

app = Flask(__name__)
app.config.from_object("project.config.Config")
app.jinja_env.autoescape = select_jinja_autoescape
app.register_blueprint(custom_jinja_blueprint)

db = SQLAlchemy(app, model_class=BaseModel)
menu = Menu(app)
user_manager = WeddingUserManager(app, db, User)
user_manager.email_adapter = MailGunEmailAdapter(app)


def admin_view(subpage_name: str):
    def is_admin():
        return current_user.has_roles("admin")

    # Helper decorator that combines the various other decorators required to create an admin view
    def decorator(func):
        # Note this is a fake page used only for the hierarchy
        @register_menu(app, ".admin", "Admin", visible_when=is_admin)
        @register_menu(app, f".admin.{subpage_name.replace(' ', '_')}", subpage_name.title(), visible_when=is_admin)
        @roles_accepted("admin")
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


def redirect_authenticated(view_function):
    @wraps(view_function)
    def decorator(*args, **kwargs):
        # User must be logged in with a confirmed email address
        is_authenticated = user_manager.call_or_get(
            current_user.is_authenticated
        ) and user_manager.db_manager.user_has_confirmed_email(current_user)

        if is_authenticated:
            # Redirect to main site
            return redirect("/home")

        return view_function(*args, **kwargs)

    return decorator


@app.errorhandler(404)
def page_not_found(_):
    return render_template("404.html.jinja2"), 404


@app.route("/")
@redirect_authenticated
def landing():
    return render_template("landing.html.jinja2")


@app.route("/home")
@login_required
@register_menu(app, ".home", "Home")
def home():
    return render_template("index.html.jinja2")


@app.route("/rsvp", methods=["GET", "POST"])
@register_menu(app, ".rsvp", "Attending")  # Note this is a fake page used only for the hierarchy
@register_menu(app, ".rsvp.rsvp", "RSVP")
@login_required
def rsvp():
    if current_user.has_roles("admin"):
        return abort(404)

    party_id = current_user.party_id
    db_state = RSVPState.init_from_party_id(party_id, db.session)
    form = db_state.build_form(request=request)

    if form.validate_on_submit():
        before_rsvp = db_state.to_frozen()
        db_state.update_db_with_form_data(form, db.session)

        # Re-fetch state from the DB to make sure the data isn't stale
        new_db_state = RSVPState.init_from_party_id(party_id, db.session)
        RSVPChange.insert(party_id, before_rsvp, new_db_state.to_frozen(), db.session)

        if not new_db_state.party.is_attending:
            return render_template("rsvp_declined.html.jinja2")
        else:
            return render_template("rsvp_accepted.html.jinja2", booking=new_db_state.booking)

    return render_template(
        "rsvp.html.jinja2", booking=db_state.booking, guests=db_state.guests, form=form, attending=db_state.attending
    )


@app.route("/accommodation")
@register_menu(app, ".rsvp", "Attending")  # Note this is a fake page used only for the hierarchy
@register_menu(app, ".rsvp.accommodation", "Accommodation")
@login_required
def accommodation():
    from project.database.accommodation import Room
    from project.database.booking import Booking
    from project.database.party import Party

    booking = Booking.get_preload(current_user.party_id, db.session)
    party: Party = db.session.query(Party).get(current_user.party_id)

    if booking is None:
        return render_template("accommodation_no_booking.html.jinja2")
    elif party.has_rsvpd and not party.is_attending:
        return render_template("accommodation_declined.html.jinja2")
    else:
        return render_template("accommodation_accepted.html.jinja2", booking=booking, party=party)


@app.route("/admin/overview")
@admin_view("overview")
def admin_overview():
    from project.database.party import Party

    statistics = RSVPStatistics(tuple(Party.get_all_preloaded(db.session)))
    return render_template("admin_overview.html.jinja2", statistics=statistics)


@app.route("/admin/party/<int:party_id>")
@roles_accepted("admin")
def admin_party(party_id: int):
    from project.database.party import Party
    from project.database.booking import Booking

    party = Party.get_preload(party_id, db.session)
    if party is None:
        return abort(404)
    else:
        booking: Booking = Booking.get_preload(party_id, db.session)
        user = User.get_by_party_id(party_id, db.session)
        return render_template("admin_party.html.jinja2", party=party, booking=booking, user=user)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
