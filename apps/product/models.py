from decimal import Decimal
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductCategory(models.Model):
    name = models.CharField(_("name"), max_length=50)

    class Meta:
        db_table = "product_category"
        verbose_name = _("product category")
        verbose_name_plural = _("product categories")

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(
        _("id"),
        editable=False,
        unique=True,
        primary_key=True,
        default=uuid.uuid4,
        db_index=True,
    )
    seller = models.ForeignKey(
        "seller.Seller",
        verbose_name=_("seller"),
        related_name="products",
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name=_("category"),
        related_name="products",
        on_delete=models.CASCADE,
    )
    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("description"), max_length=700)
    price = models.DecimalField(
        _("price"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal(0.01))],
    )
    currency = models.CharField(_("currency"), max_length=50)
    quantity = models.DecimalField(
        _("quantity"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal(0.01))],
    )
    quantity_unit = models.CharField(_("unit"), max_length=50)
    total_quantity = models.DecimalField(
        _("total quantity"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal(0.01))],
    )
    discount = models.DecimalField(
        _("percentage discount"),
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal(0.00)),
            MaxValueValidator(Decimal(100.00)),
        ],
        default=0,
    )

    is_active = models.BooleanField(_("is active"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        db_table = "product"
        verbose_name = _("product")
        verbose_name_plural = _("products")

    @property
    def new_price(self) -> float:
        if self.discount > Decimal(0):
            return self.price - (self.price * self.discount / 100)
        self.price

    @property
    def seller_name(self):
        return self.seller.user.full_name

    @property
    def state(self):
        liquid_units = ["l", "ml"]
        solid_units = ["kg", "g"]
        if self.quantity_unit in liquid_units:
            return "liquid"
        elif self.quantity_unit in solid_units:
            return "solid"
        return "pcs"

    def __str__(self) -> str:
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name=_("product"),
        related_name="images",
        on_delete=models.CASCADE,
    )
    image = models.FileField(_("image"), upload_to="product/images", max_length=200)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        db_table = "product_image"
        verbose_name = _("product image")
        verbose_name_plural = _("product images")

    def __str__(self) -> str:
        return f"{self.product.name} ;{self.order}"
