from django.shortcuts import render

from .models import FriendList, FriendRequests
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework import status

from account.models import User
from rest_framework.permissions import IsAuthenticated

'''
    Logic of this view
        - see friend list if friends 
'''
class Friend_list_view(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        # user_2= User.objects.get(id=2)
        try:
            this_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'user':'user is not exist.'})
        
        try:
            friend_list = FriendList.objects.get(user=this_user)
        except:
            return Response({'error':'Friend list query does not exist'})
        # try:
        #     if request.user != this_user:
        #         if not request.user in friend_list.friends.all():
        #             return Response({'msg':'You must be friends to view frined list.'})
                        
        friends = friend_list.friends.all().values()
        return Response(friends)
        
        # except:
        #     return Response({'Error':'Friend list does not exist.'})



'''
    Logic here to send a friend request to an user if they are not friends
'''     
class SendFriendRequests(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request, *args, **kwargs):
        user = request.user
        # user = User.objects.get(id=3) 
        receiver_user_id = self.request.query_params.get('id')

        if receiver_user_id:
            try:
                receiver = User.objects.get(id=receiver_user_id)
            except:
                return Response('receiver user:','receiver user does not exist.')

            friend_requests = FriendRequests.objects.filter(
                sender=user,receiver=receiver
            )
            
            for friend in friend_requests:
                if friend.is_active:
                    raise Exception("You already sent a friend request")
                # if none are active send a new friend request 
                friend_request = FriendRequests(sender=user, receiver=receiver)
                friend_request.save()
                return Response({'sent':'Friend Request sent successfully.'})

            friend_request = FriendRequests(sender=user,receiver=receiver)
            friend_request.save()
            return Response({'sent':'Friend Request sent successfully.'})
               
        return Response({'error':'Something went wrong'})

    

'''
    Accept friend reqeusts 
'''
class Accept_frined_request(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,*args, **kwargs):
        user = request.user
        # user = User.objects.get(id=4)

        friend_reqeust_id = self.request.query_params.get('friend_req_id')
        # print('frnd req id:',friend_reqeust_id)

        if friend_reqeust_id:
            try:
                friend_request = FriendRequests.objects.get(id=friend_reqeust_id)
                # print('friend req:',friend_request)
            except:
                return Response({'msg':'friend request not foud error.'})

            if friend_request.receiver == user:
                # print('frnd re receiver:', friend_request.receiver)
                # print('frnd re receiver id:', friend_request.receiver.id)

                if friend_request:
                    friend_request.accept()
                    return Response({"response":"Friend request accept successfullly."})
            else:
                return Response({"Error":"No such friend request"})
        else:
            return Response({"Error":"unable to accept a friend request"})


'''
    deline a friend request
'''
class DeclineFriendRequestView(APIView):
    def get(self,request,*args,**kwargs):
        # user = request.user
        user = User.objects.get(id=2)
        print('user:',user)

        friend_reqeust_id = self.request.query_params.get('friend_req_id')
        print('frnd req id:',friend_reqeust_id)

        if friend_reqeust_id:
            try:
                print('hello')
                friend_request = FriendRequests.objects.get(id=friend_reqeust_id)
                print('friend req:',friend_request)
            except:
                return Response({'msg':'friend request not foud error.'})

            if friend_request.receiver == user:
                if friend_request:
                    friend_request.decline()
                    return Response({"response":"Friend request decline successfullly."})
            else:
                return Response({"Error":"No such friend request"})
        else:
            return Response({"Error":"unable to declne a friend request"})
 