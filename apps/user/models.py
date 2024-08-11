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


def upload_pic_to(instance, filename):
    return f"users/{instance.id}/{filename}"


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    firstname = models.CharField(_("first name"), max_length=150)
    lastname = models.CharField(_("last name"), max_length=150)
    photo = models.ImageField(
        _("Photo"), upload_to=upload_pic_to, blank=True, null=True
    )
    language = models.CharField(_("language"), max_length=50)
    currency = models.CharField(_("currency"), max_length=10)

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
        refresh["role"] = self.role
        refresh["language"] = self.language
        refresh["currency"] = self.currency
        if self.role == Role.SELLER:
            try:
                seller = self.seller
                refresh["seller_id"] = str(seller.pk)
            except:
                pass
           
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

    def delete(self):
        self.photo.delete()
        super().delete()


class OTP(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otp"
    )
    code = models.CharField(_("Code"), max_length=6, blank=True, null=True)
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


class UserAddress(models.Model):
    id = models.UUIDField(
        _("id"),
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    user = models.OneToOneField(
        User,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="address",
        null=True,
    )
    street = models.CharField(_("street"), max_length=50, blank=True, null=True)
    house_number = models.CharField(
        _("house number"), max_length=10, blank=True, null=True
    )
    postal_code = models.CharField(
        _("postal code"), max_length=10, blank=True, null=True
    )
    city = models.CharField(_("city"), max_length=255, blank=True, null=True)
    country = models.CharField(_("country"), max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        db_table = "user_address"
        verbose_name = _("User Address")
        verbose_name_plural = _("User Addresses")

    def __str__(self) -> str:
        return f"{self.user.full_name} ({self.city}, {self.country})"
