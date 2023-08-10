from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name=_("Title"))
    text = models.CharField(max_length=140, verbose_name=_("Text"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        indexes = [
            models.Index(fields=["created_at"]),
        ]


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name=_("Subscriber"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.subscriber.username} follows {self.target_blog.user.username}"

    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
