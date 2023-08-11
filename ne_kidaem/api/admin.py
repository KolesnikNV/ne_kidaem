from django.contrib import admin

from blog.models import LikePost, Post, ReadPost, Subscription


admin.site.register(Post)
admin.site.register(Subscription)
admin.site.register(ReadPost)
admin.site.register(LikePost)
