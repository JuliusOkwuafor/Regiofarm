from datetime import datetime

from celery import shared_task
from decouple import config
from django.template.loader import render_to_string

from utils.exceptions import EmailNotSendException
from utils.utils import Utils
import after_response


@after_response.enable
def send_activation_email(email, firstname, uid, token):
    print('here x2')
    data = {
        "to_email": email,
        "email_subject": "Activate your account",
        "email_body": render_to_string(
            "account_activation_email.html",
            {
                "firstname": firstname,
                "domain": config("DOMAIN"),
                "uid": uid,
                "token": token,
            },
        ),
    }
    try:
        Utils.send_email(data)
    except Exception as e:
        raise EmailNotSendException(full_message=e)


@after_response.enable
def send_reset_email(email, firstname, code, otp_lifespan):
    data = {
        "to_email": email,
        "email_subject": "Reset your password",
        "email_body": render_to_string(
            "password_reset_email.html",
            {
                "firstname": firstname,
                "otp": code,
                "lifespan": otp_lifespan,
            },
        ),
    }
    try:
        Utils.send_email(data)
    except Exception as e:
        raise EmailNotSendException(full_message=e)


