from flask import (
    Flask,
    render_template_string,
    render_template,
    redirect,
)
from flask_menu import Menu, register_menu
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, login_required
from flask_login import current_user
from project.database import BaseModel
from project.database.users import User
from project.mail.mailgun import MailGunEmailAdapter

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app, model_class=BaseModel)
menu = Menu(app)
user_manager = UserManager(app, db, User)
user_manager.email_adapter = MailGunEmailAdapter(app)


def user_is_authenticated():
    db_manager = user_manager.db_manager
    return user_manager.call_or_get(current_user.is_authenticated) and db_manager.user_has_confirmed_email(current_user)


# The Home page is accessible to anyone
@app.route("/")
def landing():
    if user_is_authenticated():
        return redirect("/home")
    else:
        return render_template("landing.html")


@app.route("/home")
@login_required
@register_menu(app, ".home", "Home")
def home():
    return render_template("index.html")


@app.route("/subpage.html")
@register_menu(app, ".page", "Page With Subpages")  # Note this is a fake page used only for the hierarchy
@register_menu(app, ".page.subpage", "Subpage")
@login_required
def subpage():
    return render_template("index.html")


@app.route("/subpage2.html")
@register_menu(app, ".page", "Page With Subpages")  # Note this is a fake page used only for the hierarchy
@register_menu(app, ".page.subpage2", "Subpage 2")
@login_required
def subpage2():
    return render_template("index.html")
