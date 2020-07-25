import os
from datetime import datetime, timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/project/static"

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

    USER_FORGOT_PASSWORD_TEMPLATE = "flask_user/forgot_password.html.jinja2"
    USER_LOGIN_TEMPLATE = "flask_user/login.html.jinja2"
    USER_REGISTER_TEMPLATE = "flask_user/register.html.jinja2"
    USER_RESEND_CONFIRM_EMAIL_TEMPLATE = "flask_user/resend_confirm_email.html.jinja2"

    WEDDING_DATE = datetime.strptime("Aug 28 2021", "%b %d %Y").date()
    BOOKING_MAX_N_DAYS = 7
    BOOKING_MIN_DATE = WEDDING_DATE - timedelta(days=BOOKING_MAX_N_DAYS)
    BOOKING_MAX_DATE = WEDDING_DATE + timedelta(days=BOOKING_MAX_N_DAYS)
    RSVP_DEADLINE = datetime.strptime("Feb 1 2021", "%b %d %Y").date()

    HOUSE_LAT_LONG = (49.374088, 8.158309)
    HOUSE_ADDRESS = "Kurpfalzstrasse 152, 67435 Neustadt an der Weinstrasse"
    RESTAURANT_LAT_LONG = (49.3870215, 8.1601126)
    RESTAURANT_ADDRESS = "Deidesheimer Strasse 12, 67435 Neustadt an der Weinstrasse"
