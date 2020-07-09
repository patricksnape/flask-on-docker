import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/project/static"

    # Flask-MailGun settings
    MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN", "sandboxf49773835c1049949b8632754c0d3e1f.mailgun.org")
    MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")

    # Flask-User settings
    USER_APP_NAME = "Snape Wedding"
    USER_ENABLE_EMAIL = True
    USER_ENABLE_USERNAME = False
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = f"mailgun@{MAILGUN_DOMAIN}"
