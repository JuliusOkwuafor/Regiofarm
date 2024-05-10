import uuid

from common.models import Favorite
from django.db import models
from django.utils.translation import gettext_lazy as _


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
        "seller.Seller", verbose_name=_("author"), on_delete=models.CASCADE
    )
    headline = models.CharField(_("headline"), max_length=50)
    content = models.TextField(_("content"), max_length=1000)
    link = models.URLField(_(""), max_length=200)
    notify_followers = models.BooleanField(_("notify followers"))
    is_active = models.BooleanField(_("is active"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        db_table = "post"
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    @property
    def total_views(self) -> int:
        return self.post_view.count()

    @property
    def total_likes(self):
        return Favorite.objects.filter(object_id=self.pk).count()

    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(
        Post,
        verbose_name=_("post"),
        related_name="images",
        on_delete=models.CASCADE,
    )
    image = models.FileField(_("image"), upload_to="post/images", max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(_("is Active"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        db_table = "post_image"
        verbose_name = _("post image")
        verbose_name_plural = _("post images")

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
