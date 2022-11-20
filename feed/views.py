from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response

from .models import Feed, Post, Comment, Like
from .serializers import PostSerializers, CommentSerializers

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

'''
    Logic here to create a post
        - login(authenticate credentials will must provide)
        - user can post his own timeline
        - user has permission to post on friends timeline
            -must become friends
'''

# post create using viewset with override perform create method/function 
class PostCreateViewset(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        data = self.request.data
        # print('user name:',user)
        print('req data:',self.request.data)

        if 'feed' not in data:
            user = self.request.user
            # user = User.objects.get(id=3)  // only for check  
            print('user name:',user)

            serializer = PostSerializers(data=self.request.data)
            if serializer.is_valid():
                serializer.save(author=user,feed=user.feed_author)

        elif 'feed' in data:
            user = User.objects.get(id=3)
            print('user name:',user)

            feed_id = self.request.data['feed']
            feed = Feed.objects.get(id=feed_id)

            # check friend list for friend post
            friend_list = FriendList.objects.get(user=user)     
            friends = friend_list.friends.all()

            if feed.author in friends:
                serializer = PostSerializers(data=self.request.data)
                if serializer.is_valid():
                    serializer.save(author=user, feed = feed)

        else:
            raise serializer.ValidationError("feed or user not matched to post on timeline.")


# same logic as viewset, create post on ownself timeline and friends timeline 
class PostOnTimeLineView(generics.GenericAPIView):
    queryset =  Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticated]

    def post(self,request,*args,**kwargs):
        data = request.data
        
        if 'feed' not in data:
            user = User.objects.get(id=3)
            print('user name:',user)
            serializer = PostSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save(author=user,feed=user.feed_author)
                return Response(serializer.data)
            return Response(serializer.errors)

        else:
            user = request.user
            # user = User.objects.get(id=3)

            feed_id = request.data['feed']
            feed = Feed.objects.get(id=feed_id)

            # check friend list for friend post
            friend_list = FriendList.objects.get(user=user)     
            friends = friend_list.friends.all()

            if feed.author in friends:
                serializer = PostSerializers(data=request.data)
                if serializer.is_valid():
                    serializer.save(author=user, feed = feed)
                    return Response(serializer.data)
                return Response(serializer.errors)
            return Response({'msg':'has no permission to post on someones timeline without become a friend.'})

 
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
    permission_classes = [IsAuthenticated]

    def get(self,request,*args, **kwargs):
        user = request.user
        # user = User.objects.get(id=4)

        post_id = self.request.query_params.get('post_id')
        post = Post.objects.filter(id=post_id).first()
        
        # get request users frind list 
        friend_list = FriendList.objects.get(user=user)     
        friends = friend_list.friends.all()
        '''
            if post author in reqeust users frined list -> 
                - can like the post and dislike 
        '''
        post_by_user = post.author

        liked = True
        if post_by_user in friends:
            already_liked = Like.objects.filter(liker=user,post=post)
            if already_liked:
                return Response({'liked':liked})
            if not already_liked:
                liked_post = Like(liker=user,post=post)
                liked_post.save()
                return Response({'msg':'Your Like added successfully.'})
        else:
            return Response({'msg':'yon can not like this post.To like this post you become friends with post author.'})
        

'''
comment logics if friends post then comment on a post
'''
class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request, *args, **kwargs):
        user = request.user
        # user = User.objects.get(id=4)

        post_id = self.request.query_params.get('post_id')
        post = Post.objects.filter(id=post_id).first()

        # get request users frind list 
        friend_list = FriendList.objects.get(user=user)
        
        friends = friend_list.friends.all()
        '''
            if post author in reqeust.user frined list -> 
                - can comment on this post 
        '''
        if post.author in friends:
            data = request.data
            serializer = CommentSerializers(data=data)
            if serializer.is_valid():
                serializer.save(post=post,author=user)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response({'msg':'yon can not comment this post.To like this post you become friends with post author.'})


# like withdraw logics 
class Withdraw_like_view(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,*args, **kwargs):
        user = request.user
        # user = User.objects.get(id=4)

        post_id = self.request.query_params.get('post_id')
        post = Post.objects.filter(id=post_id).first()

        already_liked = Like.objects.filter(liker=user,post=post)
        if already_liked:
            liked = True
            already_liked.delete()
            return Response({'msg':'withdraw like successfully.','liked':liked})
        else:
            liked = False
            return Response({'Error':'No like found','liked': liked})