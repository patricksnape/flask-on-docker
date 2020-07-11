from flask import (
    Flask,
    render_template_string,
    render_template,
)
from flask_menu import Menu, register_menu
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, login_required

from project.database import BaseModel
from project.database.users import User
from project.mail.mailgun import MailGunEmailAdapter

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app, model_class=BaseModel)
menu = Menu(app)
user_manager = UserManager(app, db, User)
user_manager.email_adapter = MailGunEmailAdapter(app)


# The Home page is accessible to anyone
@app.route("/")
@register_menu(app, ".home", "Home")
def index():
    return render_template("index.html")


@app.route("/subpage.html")
@register_menu(app, ".page", "Page With Subpages")  # Note this is a fake page used only for the hierarchy
@register_menu(app, ".page.subpage", "Subpage")
def subpage():
    return render_template("layout.html")


@app.route("/subpage2.html")
@register_menu(app, ".page", "Page With Subpages")  # Note this is a fake page used only for the hierarchy
@register_menu(app, ".page.subpage2", "Subpage 2")
def subpage2():
    return render_template("layout.html")


# The Members page is only accessible to authenticated users
@app.route("/members")
@login_required  # Use of @login_required decorator
def member_page():
    return render_template_string(
        """
            {% extends "flask_user_layout.html" %}
            {% block content %}
                <h2>{%trans%}Members page{%endtrans%}</h2>
                <p><a href={{ url_for('user.register') }}>{%trans%}Register{%endtrans%}</a></p>
                <p><a href={{ url_for('user.login') }}>{%trans%}Sign in{%endtrans%}</a></p>
                <p><a href={{ url_for('home_page') }}>{%trans%}Home Page{%endtrans%}</a> (accessible to anyone)</p>
                <p><a href={{ url_for('member_page') }}>{%trans%}Member Page{%endtrans%}</a> (login_required: member@example.com / password)</p>
                <p><a href={{ url_for('user.logout') }}>{%trans%}Sign out{%endtrans%}</a></p>
            {% endblock %}
            """
    )
