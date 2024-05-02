import uuid
from datetime import datetime
from datetime import timezone as tz

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from .enums import Role
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    firstname = models.CharField(_("first name"), max_length=150)
    lastname = models.CharField(_("last name"), max_length=150)
    photo = models.ImageField(_("Photo"), upload_to="photos/", blank=True, null=True)

    is_active = models.BooleanField(_("active"), default=True)
    is_verified = models.BooleanField(_("verified"), default=False)

    role = models.CharField(
        _("role"), max_length=50, choices=Role.choices, default=Role.USER
    )
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_superuser = models.BooleanField(_("superuser status"), default=False)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstname", "lastname"]
    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    @property
    def full_name(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        db_table = "user"
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-created_at"]





class OTP(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otp"
    )
    code = models.CharField(_("Code"), max_length=4, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "otp"
        verbose_name = _("OTP")
        verbose_name_plural = _("OTPs")

    otp_lifespan = settings.OTP_LIFESPAN

    @property
    def is_expired(self) -> bool:
        lifespan = (
            (settings.OTP_LIFESPAN * 60)
            if hasattr(settings, "OTP_LIFESPAN")
            else 5 * 60
        )
        return (datetime.now(tz.utc) - self.created_at).seconds > lifespan

    def __str__(self) -> str:
        return f"{self.user.email} -- OTP: {self.code}"
