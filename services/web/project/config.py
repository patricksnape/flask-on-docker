import os
from datetime import datetime, timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

env = os.environ

class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{env['POSTGRES_USER']}:{env['POSTGRES_PASSWORD']}@{env['SQL_HOST']}:{env['SQL_PORT']}/{env['POSTGRES_DB']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Flask-MailGun settings
    MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN", "sandboxf49773835c1049949b8632754c0d3e1f.mailgun.org")
    MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY", "")

    GOOGLE_MAPS_API_TOKEN = os.getenv("GOOGLE_MAPS_API_TOKEN", "")

    # Flask-User settings
    USER_APP_NAME = "Snape Wedding"
    USER_ENABLE_EMAIL = True
    USER_ENABLE_USERNAME = False
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = f"mailgun@{MAILGUN_DOMAIN}"
    USER_AFTER_LOGIN_ENDPOINT = "home"
    USER_AFTER_REGISTER_ENDPOINT = "home"
    USER_SHOW_EMAIL_DOES_NOT_EXIST = True
    USER_USER_SESSION_EXPIRATION = timedelta(days=1).total_seconds()

    USER_FORGOT_PASSWORD_TEMPLATE = "flask_user/forgot_password.html.jinja2"
    USER_LOGIN_TEMPLATE = "flask_user/login.html.jinja2"
    USER_REGISTER_TEMPLATE = "flask_user/register.html.jinja2"
    USER_RESEND_CONFIRM_EMAIL_TEMPLATE = "flask_user/resend_confirm_email.html.jinja2"

    WEDDING_DATETIME = datetime.strptime("Aug 28 2021 13:00", "%b %d %Y %H:%M")
    BOOKING_MAX_N_DAYS = 7
    BOOKING_MIN_DATE = WEDDING_DATETIME.date() - timedelta(days=BOOKING_MAX_N_DAYS)
    BOOKING_MAX_DATE = WEDDING_DATETIME.date() + timedelta(days=BOOKING_MAX_N_DAYS)
    RSVP_DEADLINE = datetime.strptime("Feb 1 2021", "%b %d %Y").date()

    HOUSE_LAT_LONG = (49.374088, 8.158309)
    HOUSE_ADDRESS = "Kurpfalzstrasse 152, 67435 Neustadt an der Weinstrasse"
    RESTAURANT_LAT_LONG = (49.3870215, 8.1601126)
    RESTAURANT_ADDRESS = "Deidesheimer Strasse 12, 67435 Neustadt an der Weinstrasse"
