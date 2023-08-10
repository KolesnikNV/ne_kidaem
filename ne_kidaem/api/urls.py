from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import PostView, SubscriptionView, UserViewSet

router = DefaultRouter()

router.register(r"posts", PostView, basename="post")
router.register(r"subscriptions", SubscriptionView, basename="subscription")
router.register(r"user", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("token/", obtain_auth_token, name="token_obtain_pair"),
]
