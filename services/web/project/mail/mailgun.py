import smtplib
import socket

from flask import current_app
from flask_user import ConfigError, EmailError
from flask_user.email_adapters import EmailAdapterInterface


class MailGunEmailAdapter(EmailAdapterInterface):
    """ Implements the EmailAdapter interface to send emails using the Flask-MailGun API."""
    def __init__(self, app):
        """Check config settings and setup Flask-MailGun.

        Args:
            app(Flask): The Flask application instance.
        """
        super().__init__(app)

        try:
            from flask_mailgun import MailGun
        except ImportError:
            raise ConfigError(
                "The Flask-MailGun package is missing. Install Flask-Mail with 'pip install Flask-MailGun'.")
        self.mail = MailGun(app)

    def send_email_message(self, recipient, subject, html_message, text_message, sender_email, sender_name):
        """ Send email message via Flask-MailGun.

        Args:
            recipient: Email address or tuple of (Name, Email-address).
            subject: Subject line.
            html_message: The message body in HTML.
            text_message: The message body in plain text.
        """

        # Construct sender from sender_name and sender_email
        sender = '"%s" <%s>' % (sender_name, sender_email) if sender_name else sender_email

        if not current_app.testing:
            from flask_mailgun.message import Message
            message = Message(
                subject,
                sender=sender,
                recipients=[recipient],
                html=html_message,
                body=text_message)

            # Send email message
            self.mail.send(message)
