import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User
from django.core.validators import MinValueValidator

# Create your models here.


class SellerCategory(models.Model):
    name = models.CharField(
        _("name"), max_length=50, primary_key=True, editable=False, db_index=True
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        db_table = "seller_category"
        verbose_name = _("seller category")
        verbose_name_plural = _("seller categories")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Seller(models.Model):
    id = models.UUIDField(
        _("id"),
        editable=False,
        unique=True,
        primary_key=True,
        default=uuid.uuid4,
        db_index=True,
    )
    user = models.OneToOneField(
        User,
        verbose_name=_("user"),
        related_name="seller",
        on_delete=models.CASCADE,
        editable=False,
    )
    category = models.ForeignKey(
        SellerCategory,
        verbose_name=_("category"),
        related_name="seller",
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(_("company name"), max_length=255)
    ceo = models.CharField(_("company ceo"), max_length=225)
    vat = models.CharField(_("company vat"), max_length=225)
    description = models.TextField(_("description"), blank=True, null=True)
    opening_hour = models.TimeField(_("opening hour"), blank=True, null=True)
    closing_hour = models.TimeField(_("closing hour"), blank=True, null=True)
    delivery_terms_price = models.DecimalField(
        _("delivery price"), max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    delivery_terms_distance = models.DecimalField(_("delivery distance"), max_digits=10, decimal_places=1)
    latitude = models.DecimalField(_("latitude"), max_digits=9, decimal_places=6,null=True)
    longitude = models.DecimalField(_("latitude"), max_digits=9, decimal_places=6,null=True)
    # payment_methods = 

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        db_table = "seller"
        verbose_name = _("seller")
        verbose_name_plural = _("sellers")
        ordering = ["-created_at"]
