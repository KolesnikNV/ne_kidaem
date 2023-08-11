from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import (LikePostView, PostViewSet, ReadPostView, UserFeedViewSet,
                    UserViewSet,)


router = DefaultRouter()

router.register(r"posts", PostViewSet, basename="post")
router.register(r"feed", UserFeedViewSet, basename="subscription")
router.register(r"user", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("read/", ReadPostView.as_view(), name="readpost"),
    path("like/", LikePostView.as_view(), name="likepost"),
    path("token/", obtain_auth_token, name="token_obtain_pair"),
]
