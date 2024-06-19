from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Notification


@receiver(post_save, sender=Notification)
def notify_user(sender, instance: Notification, created, **kwargs):
    if created:
        print('from signal',instance.user.pk)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            str(instance.user.pk),
            {
                "type": "notify",
                "message": {
                    "id": instance.id,
                    "title": instance.title,
                    "message": instance.message,
                    "is_read": instance.is_read,
                },
            },
        )

