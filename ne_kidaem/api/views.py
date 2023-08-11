from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth.models import User
from django.db.models import OuterRef, Subquery
from django.shortcuts import get_object_or_404

from blog.models import LikePost, Post, ReadPost, Subscription

from .constants import (ERROR_ALREADY_LIKE, ERROR_ALREADY_READ,
                        ERROR_ALREADY_SUBSCRIBED, ERROR_NOT_SUBSCRIBED,
                        ERROR_SUBSCRIBE_SELF, POST_IS_LIKE, POST_IS_READ,)
from .serializers import PostSerializer, UserSerializer


class PostViewSet(ModelViewSet):
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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    @action(detail=True, methods=["post"])
    def read(self, request, pk=None):
        post = self.get_object()

        _, created = ReadPost.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response(
                {"detail": f"{ERROR_ALREADY_READ}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"detail": f"{POST_IS_READ}"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()

        _, created = LikePost.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response(
                {"detail": f"{ERROR_ALREADY_LIKE}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"detail": f"{POST_IS_LIKE}"}, status=status.HTTP_200_OK)


class UserFeedViewSet(ModelViewSet):
    queryset = Subscription.objects.annotate(
        last_post_created_at=Subquery(
            Post.objects.filter(author=OuterRef("author"))
            .order_by("-created_at")
            .values("created_at")
        )
    )

    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        user = request.user
        subscribed_blogs = user.subscriptions.values_list("author", flat=True)
        posts = Post.objects.filter(author__in=subscribed_blogs).order_by("-created_at")
        paginated_posts = self.paginate_queryset(posts)
        serializer = PostSerializer(
            paginated_posts, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)


class ReadPostView(APIView):
    def get(self, request):
        read_posts = ReadPost.objects.filter(user=request.user).values_list(
            "post", flat=True
        )

        user_posts = Post.objects.filter(id__in=read_posts)
        serialized_posts = PostSerializer(
            user_posts, many=True, context={"request": request}
        ).data

        for post in serialized_posts:
            post["is_read"] = post["id"] in read_posts

        return Response(serialized_posts, status=status.HTTP_200_OK)


class LikePostView(APIView):
    def get(self, request):
        read_posts = LikePost.objects.filter(user=request.user).values_list(
            "post", flat=True
        )

        user_posts = Post.objects.filter(id__in=read_posts)
        serialized_posts = PostSerializer(
            user_posts, many=True, context={"request": request}
        ).data

        for post in serialized_posts:
            post["is_like"] = post["id"] in read_posts

        return Response(serialized_posts, status=status.HTTP_200_OK)


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
