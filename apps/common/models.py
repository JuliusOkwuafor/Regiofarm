import uuid
from decimal import Decimal

from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .enums import OrderStatus, PaymentMethod


class Favorite(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        "contenttypes.ContentType", on_delete=models.CASCADE
    )
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "favorite"
        verbose_name = _("favorite")
        verbose_name_plural = _("favorites")
        unique_together = (("user", "content_type", "object_id"),)
        index_together = ("content_type", "object_id")

    def __str__(self):
        # return str(self.pk)
        return f"{self.user.email} -> {self.content_type.name}"


class Order(models.Model):
    id = models.UUIDField(
        _("id"),
        editable=False,
        unique=True,
        primary_key=True,
        default=uuid.uuid4,
        db_index=True,
    )
    owner = models.ForeignKey(
        "user.User",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="order",
    )
    seller = models.ForeignKey(
        "seller.Seller",
        verbose_name=_("Seller"),
        on_delete=models.CASCADE,
        related_name="order",
    )
    tip = models.DecimalField(
        _("tip"),
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal(0.01))],
    )
    status = models.CharField(
        _("order status"),
        max_length=50,
        choices=OrderStatus.choices,
        default=OrderStatus.PROCESSING,
    )
    payment_method = models.CharField(
        _("payment method"),
        max_length=50,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH,
    )
    note = models.TextField(_("note"), blank=True, null=True)
    placed_at = models.DateTimeField(_("date placed"), auto_now_add=True)

    class Meta:
        db_table = "order"
        verbose_name = _("order")
        verbose_name_plural = _("orders")
        ordering = ["-placed_at"]

    def __str__(self):
        return f"{self.owner.email} -> {self.seller.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name=_("order"),
        on_delete=models.CASCADE,
        related_name="order_item",
    )
    product = models.ForeignKey(
        "product.Product",
        verbose_name=_("Product"),
        on_delete=models.CASCADE,
        related_name="order_item",
    )
    quantity = models.PositiveIntegerField(
        _("quantity"), default=1, validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(
        _("price"),
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal(0.01))],
    )

    class Meta:
        db_table = "order_item"
        verbose_name = _("order item")
        verbose_name_plural = _("order items")

    def __str__(self):
        return f"{self.order.owner.email} -> {self.product.name}"
