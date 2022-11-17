from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response

from .models import Feed, Post, Comment, Like
from .serializers import PostSerializers, CommentSerializers

from rest_framework import viewsets, mixins

class PostCreateViewset(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers

    def perform_create(self, serializer):
        if hasattr(self.request.user,'feed_author'):
            serializer.save(author=self.request.user.feed_user,feed=self.request.user)
        elif self.request.user:
            serializer.save(author=self.request.user, feed = self.request.data['feed_id'])
        else:
            raise serializer.ValidationError("feed not matched.")

