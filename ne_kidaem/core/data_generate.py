from django.contrib.auth.models import User
from loguru import logger
from mixer.backend.django import mixer


def create_users():
    for _ in range(100):
        username = mixer.faker.user_name()
        email = mixer.faker.email()
        password = mixer.faker.password()
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        logger.info("User {user.username} created")
