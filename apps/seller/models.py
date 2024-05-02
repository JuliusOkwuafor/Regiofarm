import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User

# Create your models here.


class SellerProfile(models.Model):
    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, verbose_name=_("user"), on_delete=models.CASCADE, related_name="seller"
    )
    company_name = models.CharField(_("company name"), max_length=255)
    company_ceo = models.CharField(_("company ceo"), max_length=225)
    company_street = models.CharField(_("company street"), max_length=255)
    company_house_number = models.CharField(_("company house number"), max_length=10)
    company_postal_code = models.CharField(_("company postal code"), max_length=10)
    company_city = models.CharField(_("company city"), max_length=255)
    company_country = models.CharField(_("company country"), max_length=255)
    company_vat_id = models.CharField(_("company vat id"), max_length=50)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = "seller_profile"
        verbose_name = _("seller profile")
        verbose_name_plural = _("seller profiles")
        ordering = ["-created_at"]
