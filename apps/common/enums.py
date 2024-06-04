from django.db.models import TextChoices


class OrderStatus(TextChoices):
    PROCESSING = "processing", "processing"
    ON_THE_WAY = "on_the_way", "on the way"
    READY = "ready", "ready"
    CANCELED = "canceled", "canceled"
    DELIVERED = "delivered", "delivered"


class PaymentMethod(TextChoices):
    CASH = "cash", "cash"
    CARD = "card", "card"
    PAYPAL = "paypal", "paypal"
    BANK_TRANSFER = "bank_transfer", "bank transfer"
