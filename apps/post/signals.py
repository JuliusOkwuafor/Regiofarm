from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from notification.models import Notification
from common.models import Favorite
from seller.models import Seller
from django.contrib.contenttypes.models import ContentType


@receiver(post_save, sender=Post)
def notify_favorites_on_post_save(sender, instance: Post, created, **kwargs):
    if created:
        if instance.notify_followers:
            favorite_users = Favorite.objects.filter(
                content_type=ContentType.objects.get_for_model(Seller),
                object_id=instance.author.id,
            )
            for favorite in favorite_users:
                Notification.objects.create(
                    user=favorite.user,
                    title=f"{instance.author.name} has added a new post",
                    message=instance.headline,
                )
