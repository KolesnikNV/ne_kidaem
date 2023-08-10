from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from blog.models import Post, Subscription

from .serializers import PostSerializer, SubscriptionSerializer, UserSerializer

ERROR_SUBSCRIBE_SELF = "Нельзя подписаться на себя"
ERROR_ALREADY_SUBSCRIBED = "Вы уже подписаны на данного автора"
ERROR_NOT_SUBSCRIBED = "Вы не подписаны на данного автора"


class PostView(ModelViewSet):
    queryset = Post.objects.select_related("author")
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs["pk"])
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs["pk"])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionView(ModelViewSet):
    queryset = Subscription.objects.select_related("author").prefetch_related(
        "author__post_set"
    )
    serializer_class = SubscriptionSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["post"])
    def subscribe(self, request, pk=None):
        user_to_subscribe = self.get_object()

        # Check if the user is trying to subscribe to themselves
        if request.user == user_to_subscribe:
            return Response(
                {"detail": "You cannot subscribe to yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if existing_subscription := Subscription.objects.filter(
            subscriber=request.user, author=user_to_subscribe
        ).first():
            return Response(
                {"detail": "You are already subscribed to this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription = Subscription(subscriber=request.user, author=user_to_subscribe)
        subscription.save()
        return Response(
            {"detail": "Subscribed successfully."}, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["get"])
    def posts(self, request, pk=None):
        user_posts = Post.objects.filter(author=pk)
        serializer = PostSerializer(user_posts, many=True)
        return Response(serializer.data)
