
from rest_framework import serializers
from .models import Feed, Comment,Post,Like

class PostSerializers(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('content','feed')

class CommentSerializers(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['content']