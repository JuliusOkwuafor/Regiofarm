from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _


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
