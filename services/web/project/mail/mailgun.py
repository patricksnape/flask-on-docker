from __future__ import annotations

from typing import Tuple, Optional

from flask import current_app, Flask
from flask_mailgun import MailGun
from flask_mailgun.message import Message
from flask_user.email_adapters import EmailAdapterInterface


class MailGunEmailAdapter(EmailAdapterInterface):
    def __init__(self, app: Flask) -> None:
        super().__init__(app)
        self.mail = MailGun(app)

    def send_email_message(
        self,
        recipient: Tuple[str, str],
        subject: str,
        html_message: str,
        text_message: str,
        sender_email: Optional[str],
        sender_name: Optional[str],
    ) -> None:
        # TODO: sender_name is unused as it needs to be propagated through the MailGun API
        if not current_app.testing:
            message = Message(
                subject, sender=sender_email, recipients=[recipient], html=html_message, body=text_message
            )

            # Send email message
            self.mail.send(message)
