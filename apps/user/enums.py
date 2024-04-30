from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class Role(TextChoices):
    ADMIN = "admin", _("admin")
    USER = "user", _("user")
    SELLER = "seller", _("seller")
