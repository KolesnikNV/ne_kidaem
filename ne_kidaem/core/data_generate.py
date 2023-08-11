from loguru import logger
from mixer.backend.django import mixer

from django.contrib.auth.models import User

from blog.models import Post


def create_users():
    for _ in range(100):
        username = mixer.faker.user_name()
        email = mixer.faker.email()
        password = mixer.faker.password()
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        logger.info(f"User {user.username} created")


def create_posts():
    users = User.objects.all()
    for user in users:
        for _ in range(100):
            title = mixer.faker.sentence()
            text = mixer.faker.text()
            created_at = mixer.faker.date_time_this_year()
            post = Post(title=title, text=text, created_at=created_at, author=user)
            post.save()
            logger.info(f"Post '{post.title}' created for user '{user.username}'")
