from celery import shared_task

from django.core.mail import send_mail
from django.utils.html import strip_tags

from blog.models import Post, Subscription


@shared_task
def send_daily_post_digest():
    users = Subscription.objects.select_related("user", "author").all()

    for user in users:
        if posts := Post.objects.filter(author=user.author).order_by("-created_at")[:5]:
            subject = "Ежедневная подборка постов"
            message = "Новая подборка!".join(
                f"{post.title}\n{post.text}\n\n" for post in posts
            )
            send_mail(
                subject,
                strip_tags(message),
                "your_email@example.com",
                [user.user.email],
                html_message=message,
            )
