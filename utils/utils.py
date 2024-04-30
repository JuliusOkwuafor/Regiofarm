import threading
from django.core.mail import EmailMessage
from django.conf import settings


class Utils:
    @staticmethod
    def send_email(data) -> None:
        email = EmailMessage(
            subject=data["email_subject"],
            body=data["email_body"],
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[data["to_email"]],
        )
        # EmailThread(email).start()
        email.send()

class EmailThread(threading.Thread):
    def __init__(self, email) -> None:
        self.email = email
        threading.Thread.__init__(self)

    def run(self) -> None:
        self.email.send()