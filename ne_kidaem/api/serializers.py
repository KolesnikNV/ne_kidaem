from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Post, Subscription


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    created_at = serializers.DateTimeField(format="%d-%m-%Y в %H:%M", read_only=True)

    class Meta:
        model = Post
        fields = ["title", "text", "created_at", "author"]


class PostsForSubscribers(serializers.Serializer):
    title = serializers.CharField(source="title")
    text = serializers.CharField(source="text")
    created_at = serializers.DateTimeField(
        format="%d-%m-%Y в %H:%M", source="created_at"
    )


class SubscriptionSerializer(serializers.ModelSerializer):
    posts = PostsForSubscribers(many=True, source="author.post_set")
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Subscription
        fields = ["author", "posts"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
