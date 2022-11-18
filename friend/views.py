from django.shortcuts import render

from .models import FriendList, FriendRequests
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework import status

from account.models import User

class Friend_list_view(APIView):

    def get(self,request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            this_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'user:','user is not exist.'})
        
        friend_list = FriendList.objects.get(user=this_user)
        
        if request.user != this_user:
            if not request.user in friend_list.friends.all():
                return Response({'msg':'You must be friends to view frined list.'})
        
        friends = []
        auth_user_friend_list =FriendList.objects.get(user=request.user)

        for friend in friend_list.friends.all():
            friends.append((friends, auth_user_friend_list.is_mutual_friend(friend)))
        return Response({
            'friends':friends
        })