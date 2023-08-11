from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from blog.models import Post, ReadPost, Subscription

from .constants import (
    ERROR_ALREADY_SUBSCRIBED,
    ERROR_NOT_SUBSCRIBED,
    ERROR_SUBSCRIBE_SELF,
    ERROR_ALREADY_READ,
    POST_IS_READ,
)
from .serializers import PostSerializer, SubscriptionSerializer, UserSerializer


class PostView(ModelViewSet):
    queryset = Post.objects.select_related("author")
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        subscribed_authors = user.subscriptions.values_list("author_id", flat=True)
        return Post.objects.filter(author__in=subscribed_authors)

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

    @action(detail=True, methods=["get"])
    def read(self, request, pk=None):
        post = self.get_object()
        _, created = ReadPost.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response(
                {"detail": f"{ERROR_ALREADY_READ}"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"detail": f"{POST_IS_READ}"}, status=status.HTTP_200_OK)


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

        if request.user == user_to_subscribe:
            return Response(
                {"detail": f"{ERROR_SUBSCRIBE_SELF}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if existing_subscription := Subscription.objects.filter(
            subscriber=request.user, author=user_to_subscribe
        ).first():
            return Response(
                {"detail": f"{ERROR_ALREADY_SUBSCRIBED}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription = Subscription(subscriber=request.user, author=user_to_subscribe)
        subscription.save()
        return Response(
            {"detail": f"{ERROR_NOT_SUBSCRIBED}"}, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["get"])
    def posts(self, request, pk=None):
        user_posts = Post.objects.filter(author=pk)
        serializer = PostSerializer(user_posts, many=True)
        return Response(serializer.data)
