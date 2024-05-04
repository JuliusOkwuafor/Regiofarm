import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User

# Create your models here.


class SellerProfile(models.Model):
    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="sellerprofile",
    )
    company_name = models.CharField(_("company name"), max_length=255)
    company_ceo = models.CharField(_("company ceo"), max_length=225)
    company_vat_id = models.CharField(_("company vat"), max_length=225)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = "seller_profile"
        verbose_name = _("seller profile")
        verbose_name_plural = _("seller profiles")
        ordering = ["-created_at"]


class SellerCategory(models.Model):
    name = models.CharField(_("name"), max_length=50)
    icon = models.FileField(_("icon"), upload_to="seller/category", max_length=200)

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
    )
    category = models.ForeignKey(
        SellerCategory,
        verbose_name=_("category"),
        related_name="seller",
        on_delete=models.CASCADE,
    )
    name = models.CharField(_("name"), max_length=50)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        db_table = "seller"
        verbose_name = _("seller")
        verbose_name_plural = _("sellers")
        ordering = ["-created_at"]
