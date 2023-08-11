from rest_framework import serializers

from django.contrib.auth.models import User

from blog.models import Post, ReadPost, Subscription


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    created_at = serializers.DateTimeField(format="%d-%m-%Y в %H:%M", read_only=True)
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["title", "text", "created_at", "author", "is_read"]

    def get_is_read(self, obj):
        user = self.context["request"].user
        return ReadPost.objects.filter(user=user, post=obj).exists()


class PostsForSubscribers(serializers.Serializer):
    title = serializers.CharField()
    text = serializers.CharField()
    created_at = serializers.DateTimeField(format="%d-%m-%Y в %H:%M")


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
