from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .utils import activation_token

from utils.exceptions import EmailNotSendException

from user.models import User, OTP, UserAddress
from .tasks import (
    send_activation_email as activation_mail,
    send_reset_email as reset_email,
)


@receiver(post_save, sender=User)
def send_activation_email(sender, instance: User, created, **kwargs):
    if created:
        print(sender.is_verified)
        if instance.role == "user":
            UserAddress.objects.create(user=instance)
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        token = activation_token.make_token(instance)
        print("here")
        try:
            activation_mail(
                instance.email,
                instance.firstname,
                uid,
                token,
            )
        except EmailNotSendException as e:
            # TODO: Log the error and handle it properly
            print("Email not sent due to {}".format(e.__cause__))


@receiver(post_save, sender=OTP)
def send_reset_email(sender, instance, created, **kwargs):
    if created:
        try:
            reset_email.delay(
                instance.user.email,
                instance.user.firstname,
                instance.code,
                instance.otp_lifespan,
            )
        except EmailNotSendException as e:
            # TODO: Log the error and handle it properly
            print("Email not sent due to\n{}".format(e.full_message))
