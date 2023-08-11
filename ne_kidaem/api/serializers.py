from rest_framework import serializers

from django.contrib.auth.models import User

from blog.models import LikePost, Post, ReadPost, Subscription


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    created_at = serializers.DateTimeField(format="%d-%m-%Y в %H:%M", read_only=True)
    is_read = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "title", "text", "created_at", "author", "is_read", "is_like"]

    def get_is_read(self, obj):
        user = self.context["request"].user
        return ReadPost.objects.filter(user=user, post=obj).exists()

    def get_is_like(self, obj):
        user = self.context["request"].user
        return LikePost.objects.filter(user=user, post=obj).exists()


class PostsForSubscribers(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ["id", "author"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
