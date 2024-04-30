import threading
from typing import Any

from django.conf import settings
from django.core.mail import EmailMessage


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

    @staticmethod
    def get_or_none(model: Any, **kwargs) -> Any | None:
        """
        This function returns an instance of a model if it exists, otherwise None.

        Args:
            model: The model class to query.
            **kwargs: The query parameters.

        Returns:
            An instance of the model if it exists, otherwise None.
        """
        try:
            return model.objects.get(**kwargs)
        except model.DoesNotExist:
            return None
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """
        This function validates a password based on certain criteria.

        Args:
            password: The password string to be validated.

        Returns:
            True if the password is valid, False otherwise.
        """

        # Minimum length requirement
        if len(password) < 8:
            return False

        # Character class requirements (at least one from each)
        has_uppercase = any(char.isupper() for char in password)
        has_lowercase = any(char.islower() for char in password)
        has_number = any(char.isdigit() for char in password)
        has_symbol = any(char in "!@#$%^&*()" for char in password)

        # Check if all character class requirements are met
        if not (has_uppercase and has_lowercase and has_number and has_symbol):
            return False

        return True


class EmailThread(threading.Thread):
    def __init__(self, email) -> None:
        self.email = email
        threading.Thread.__init__(self)

    def run(self) -> None:
        self.email.send()
