import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User
from seller.models import Seller

# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(_("name"), max_length=50)
    icon = models.FileField(_("icon"), upload_to="product/category", max_length=200)

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
        Seller,
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
        validators=[MinValueValidator(0.01)],
    )
    currency = models.CharField(_("currency"), max_length=50)
    quantity = models.DecimalField(
        _("quantity"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    quantity_unit = models.CharField(_("unit"), max_length=50)
    total_quantity = models.DecimalField(
        _("quantity"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    discount = models.DecimalField(
        _("percentage discount"),
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
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
        return self.price - (self.price * self.discount / 100)

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


class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "favorite_product"
        verbose_name = _("favorite product")
        verbose_name_plural = _("favorites product")

    def __str__(self):
        return f"{self.user.email} -> {self.product.name}"
