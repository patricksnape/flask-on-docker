from functools import wraps

from flask import (
    Flask,
    render_template,
    redirect,
    request,
)
from flask_login import current_user
from flask_menu import Menu, register_menu
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required

from project.database import BaseModel
from project.database.party import Party
from project.database.users import User
from project.mail.mailgun import MailGunEmailAdapter
from project.rsvp.forms import RSVPForm
from project.user_flow.user_manager import WeddingUserManager

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app, model_class=BaseModel)
menu = Menu(app)
user_manager = WeddingUserManager(app, db, User)
user_manager.email_adapter = MailGunEmailAdapter(app)


def redirect_authenticated(view_function):
    @wraps(view_function)  # Tells debuggers that is is a function wrapper
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


@app.route("/")
@redirect_authenticated
def landing():
    return render_template("landing.html")


@app.route("/home")
@login_required
@register_menu(app, ".home", "Home")
def home():
    return render_template("index.html")


@app.route("/rsvp", methods=["GET", "POST"])
@register_menu(app, ".rsvp", "RSVP")
@login_required
def rsvp():
    party = db.session.query(Party).get(current_user.party_id)
    guests = party.guests

    any_guest_confirmed = any(g.attending for g in guests)
    form = RSVPForm(request.form)
    form.guests_attending.choices = [(g.id, g.full_name) for g in guests]

    if request.method == "GET":
        form.guests_attending.default = [g.id for g in guests if g.attending is not False]
        if any(g.attending is not None for g in guests):
            form.attending.default = any_guest_confirmed
        form.process()

    if form.validate_on_submit():
        guests_attending = form.guests_attending.data
        for guest in guests:
            # The "in" is a linear search but the number of guests is always < 3
            guest.attending = guest.id in guests_attending and form.attending.data

        db.session.add_all(guests)
        db.session.commit()
        return redirect("rsvp")

    return render_template("rsvp.html", guests=guests, form=form, attending=any_guest_confirmed)


@app.route("/subpage")
@register_menu(app, ".page", "Page With Subpages")  # Note this is a fake page used only for the hierarchy
@register_menu(app, ".page.subpage", "Subpage")
@login_required
def subpage():
    return render_template("index.html")


@app.route("/subpage2")
@register_menu(app, ".page", "Page With Subpages")  # Note this is a fake page used only for the hierarchy
@register_menu(app, ".page.subpage2", "Subpage 2")
@login_required
def subpage2():
    return render_template("index.html")
