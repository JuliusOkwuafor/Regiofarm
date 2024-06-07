from decimal import Decimal
import uuid
from datetime import datetime, time, timezone

from common.models import Favorite
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from product.models import Product
from user.models import User
from .managers import SellerVerifiedManager

def upload_to(instance, filename):
    return f'seller/{instance.seller.id}/{filename}'


class SellerCategory(models.Model):
    name = models.CharField(
        _("name"), max_length=50, primary_key=True, editable=True, db_index=True
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
    )
    category = models.ForeignKey(
        SellerCategory,
        verbose_name=_("category"),
        related_name="seller",
        on_delete=models.CASCADE,
    )
    profile_image = models.ImageField(
        _("profile photo"),
        blank=True,
        null=True,
        upload_to="seller/",
        height_field=None,
        width_field=None,
        max_length=None,
    )
    cover_image = models.ImageField(
        _("cover photo"),
        blank=True,
        null=True,
        upload_to="seller/",
        height_field=None,
        width_field=None,
        max_length=None,
    )
    name = models.CharField(_("company name"), max_length=255)
    ceo = models.CharField(_("company ceo"), max_length=225)
    vat = models.CharField(_("company vat"), max_length=225)
    description = models.TextField(_("description"), blank=True)
    opening_hour = models.TimeField(_("opening hour"), blank=True, null=True)
    closing_hour = models.TimeField(_("closing hour"), blank=True, null=True)
    delivery_terms_price = models.DecimalField(
        _("delivery price"),
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal(0.01))],
    )
    delivery_terms_distance = models.DecimalField(
        _("delivery distance"), blank=True, null=True, max_digits=10, decimal_places=1
    )
    latitude = models.DecimalField(
        _("latitude"), blank=True, null=True, max_digits=9, decimal_places=6
    )
    longitude = models.DecimalField(
        _("longitude"), blank=True, null=True, max_digits=9, decimal_places=6
    )
    # link = models.URLField(_("link"), max_length=1000)
    product_discount = models.DecimalField(
        _("discount all product"),
        blank=True,
        null=True,
        max_digits=4,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal(0.00)),
            MaxValueValidator(Decimal(100.00)),
        ],
    )
    is_active = models.BooleanField(_("is active"), default=True)
    is_subscribed = models.BooleanField(_("is subscribed"), default=False)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    objects = models.Manager()
    is_verified = SellerVerifiedManager()

    class Meta:
        db_table = "seller"
        verbose_name = _("seller")
        verbose_name_plural = _("sellers")
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if self.product_discount and self.product_discount > 0:
            for product in Product.objects.filter(seller=self):
                product.discount = self.product_discount
                product.save()
        super().save(*args, **kwargs)

    @property
    def is_open(self):
        now = datetime.now(timezone.utc).time()
        if self.opening_hour and self.closing_hour:
            return self.opening_hour <= now <= self.closing_hour
        return False

    def total_likes(self):
        return Favorite.objects.filter(object_id=self.pk).count()

    def __str__(self):
        return self.name
