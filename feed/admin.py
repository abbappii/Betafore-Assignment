from django.contrib import admin

from .models import Feed, Post, Comment, Like

admin.site.register(Feed)

admin.site.register(Post)

admin.site.register(Comment)

admin.site.register(Like)

