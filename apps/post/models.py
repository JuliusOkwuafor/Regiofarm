import uuid
from typing import Any

from common.models import Favorite
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator


def upload_to(instance, filename):
    return f"post/{instance.post.id}/{filename}"


class Post(models.Model):
    id = models.UUIDField(
        _("id"),
        editable=False,
        unique=True,
        primary_key=True,
        default=uuid.uuid4,
        db_index=True,
    )
    author = models.ForeignKey(
        "seller.Seller",
        verbose_name=_("author"),
        related_name="post",
        on_delete=models.CASCADE,
    )
    headline = models.CharField(_("headline"), max_length=50)
    content = models.TextField(_("content"), validators=[MaxLengthValidator(1000)])
    link = models.URLField(_("link"), max_length=250, blank=True, null=True)
    notify_followers = models.BooleanField(_("notify followers"), default=False)
    is_active = models.BooleanField(_("is active"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    # objects = models.Manager()

    class Meta:
        db_table = "news"
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    @property
    def total_views(self) -> int:
        return self.post_view.count()

    @property
    def total_likes(self):
        return Favorite.objects.filter(object_id=self.pk).count()

    @property
    def author_name(self):
        return self.author.user.full_name

    @property
    def author_city(self):
        if self.author.user.address:
            return self.author.user.address.city
        return None

    def __str__(self):
        return self.headline


class PostImage(models.Model):
    post = models.ForeignKey(
        Post,
        verbose_name=_("post"),
        related_name="images",
        on_delete=models.CASCADE,
    )
    image = models.FileField(_("image"), upload_to=upload_to, max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(_("is Active"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        db_table = "post_image"
        verbose_name = _("post image")
        verbose_name_plural = _("post images")

    def delete(
        self, using: Any = ..., keep_parents: bool = ...
    ) -> tuple[int, dict[str, int]]:
        self.image.delete()
        return super().delete(using, keep_parents)

    def __str__(self) -> str:
        return f"{self.post.headline} ;{self.order}"


class PostView(models.Model):
    user = models.ForeignKey(
        "user.User",
        verbose_name=_("user"),
        on_delete=models.DO_NOTHING,
        related_name="post_view",
    )
    post = models.ForeignKey(
        Post,
        verbose_name=_("post"),
        on_delete=models.CASCADE,
        related_name="post_view",
    )
    created_at = models.DateTimeField(_("timestamp"), auto_now_add=True)

    class Meta:
        db_table = "post_view"
        verbose_name = _("post view")
        verbose_name_plural = _("post views")

    def __str__(self) -> str:
        return f"{self.user} viewed {self.post}"
