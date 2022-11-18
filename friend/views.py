from django.shortcuts import render

from .models import FriendList, FriendRequests
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework import status

from account.models import User

'''
    Logic of this view
        - see friend list if friends 
'''
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
        
        
'''
    Logic here to send a friend request to an user if they are not friends
'''     
class SendFriendRequests(APIView):

    def post(self,request, *args, **kwargs):
        user = request.user
        receiver_user_id = self.request.query_params.get('id')

        if receiver_user_id:
            receiver = User.objects.get(id=receiver_user_id)

            try:
                friend_requests = FriendRequests.objects.filter(
                    sender=user,receiver=receiver
                )

                try:
                    for friend in friend_requests:
                        if friend.is_active:
                            raise Exception("You already sent a friend request")
                        # if none are active send a new friend request 
                        friend_request = FriendRequests(sender=user, receiver=receiver)
                        friend_request.save()
                        return Response({'sent:','Friend Request sent successfully.'})

                except Exception as e:
                    pass 

            except FriendRequests.DoesNotExist:
                friend_request = FriendRequests(sender=user,receiver=receiver)
                friend_request.save()
                return Response({'sent:','Friend Request sent successfully.'})
        
        else:
            return Response({'error:''Something went wrong'})