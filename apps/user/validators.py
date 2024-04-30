from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from utils.utils import Utils


def password_validator(value: str):
    if not Utils.validate_password(value):
        raise ValidationError(_("The password is not valid"))
