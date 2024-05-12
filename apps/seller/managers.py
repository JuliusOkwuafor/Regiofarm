from django.db.models import Manager
from django.db.models.query import QuerySet


class SellerVerifiedManager(Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_active=True, is_subscribed=True)


class SellerManager(Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset()
