from rest_framework import status


class EmailNotSendException(Exception):
    def __init__(self, full_message, message="Email not sent"):
        self.message: str = message
        self.full_message: str = f"error: {full_message}"
        super().__init__(self.message)

    def __str__(self):
        return self.message

    def __repr__(self) -> str:
        return self.full_message


class InvalidTokenException(Exception):
    def __init__(self, full_message, message="Invalid or Expired Token"):
        self.message: str = message
        self.full_message: str = f"error: {full_message}"
        super().__init__(self.message)

    def __str__(self):
        return self.message

    def __repr__(self) -> str:
        return self.full_message

class HttpException(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self):
        return self.message

    def __repr__(self) -> str:
        return self.message + " - Status Code: " + str(self.status_code)
    
class AuthException(Exception):
    """Base class for all google.auth errors."""

    def __init__(self, *args, **kwargs):
        super(AuthException, self).__init__(*args)
        retryable = kwargs.get("retryable", False)
        self._retryable = retryable
    
    @property
    def retryable(self):
        return self._retryable