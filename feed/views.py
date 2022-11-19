from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response

from .models import Feed, Post, Comment, Like
from .serializers import PostSerializers, CommentSerializers

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

class PostCreateViewset(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if hasattr(self.request.user,'feed_author'):
            serializer.save(author=self.request.user.feed_user,feed=self.request.user)
        elif self.request.user:
            serializer.save(author=self.request.user, feed = self.request.data['feed_id'])
        else:
            raise serializer.ValidationError("feed not matched.")

 
'''
    logic need to implement 
        - like in a friend post
        - unlike if post already has a like
        - comment on friends post
'''

from friend.models import FriendList
from rest_framework.views import APIView
from account.models import User

class Like_View(APIView):

    def get(self,request,*args, **kwargs):
        # user = request.user
        user = User.objects.get(id=4)

        post_id = self.request.query_params.get('post_id')
        post = Post.objects.filter(id=post_id).first()
        if post:
            print('post user:',post.author)
        else:
            print('no post found')
        
        # get request users frind list 
        friend_list = FriendList.objects.get(user=user)
        print('frined list of post author:',friend_list)
        
        friends = friend_list.friends.all()
        print('all friends :', friends)
        for i in friends:
            print(i.friend_list_user)

        '''
            if post author in reqeust users frined list -> 
               
                - can like the post and dislike 
        '''
        post_by_user = post.author
        print('post by author:',post_by_user)

        if post_by_user in friends:
            already_liked = Like.objects.filter(liker=user,post=post)
            if already_liked:
                return Response({'liked':'True'})
            if not already_liked:
                liked_post = Like(liker=user,post=post)
                liked_post.save()
                return Response({'msg':'Your Like added successfully.'})
        else:
            return Response({'msg':'yon can not like this post.To like this post you become friends with post author.'})
        
