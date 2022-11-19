from django.shortcuts import render

from .models import User
from .serializers import LoginSerializerUser, UserListSerializers, UserRegisterSerializers, OtpVerifySerializers

from rest_framework.response import Response

from rest_framework import generics
from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.db.models import Q 
from rest_framework.views import APIView
from feed.models import Feed
from friend.models import FriendList

# This class used to register a user 
class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializers

    def post(self,request, *args, **kwargs):
        
        serializer = UserRegisterSerializers(data=request.data)
        if serializer.is_valid():
            """
                serializer will check
                    -unique email
                    -validated user will be saved
            """

            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            # confirm_password = serializer.validated_data['confirm_password']


            if User.objects.filter(email=email).exists():
                return Response({'Error':'Email Already in Used.'},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                    )
                   
            # elif password != confirm_password:
            #     return Response({'Error':"Password didn't mathched."},
            #     status=status.HTTP_406_NOT_ACCEPTABLE
            #     )
            
            else:
                authinfo = {
                    'username': username,
                    'email':email,
                    'password':make_password(password)
                }
                user =User(**authinfo)
                user.save()

                # feed save with register user 
                feed_auth = User.objects.filter(email=email).first()
                print('feed auth:',feed_auth)

                feedInfo = {
                    'author': feed_auth,
                    'slug': f'{feed_auth.username}-slug'
                }
                feed = Feed(**feedInfo)
                feed.save()
                print('feed from db:',Feed.objects.get(author=feed.author))

                # friend list create with register user email 
                friendList_auth = User.objects.get(email=email)
                friendListInfo = {
                    'user': friendList_auth
                }
                friendLIst = FriendList(**friendListInfo)
                friendLIst.save()

                return Response({"Success":"User Created Successfully."},
                    status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)




# user login view 
import random
class UserLoginOtpSendView(generics.GenericAPIView):
    serializer_class = LoginSerializerUser

    def post(self, request, *args, **kwargs):
        get_email  = request.data['email']
        password = request.data['password']
        print('get_email:',get_email)
        print('password:', password)

        get_user = User.objects.filter(email=get_email).first()

        if get_user:
            otp = random.randint(111111,999999)
            get_user.otp = otp 
            get_user.save()

            return Response({
                'OK':'Email found',
                'user_id': get_user.id
            })

        else:
            return Response(
                {'Error':'No such User Found'},
                status=status.HTTP_204_NO_CONTENT)

class UserLoginOtpVerifyView(generics.GenericAPIView):
    serializer_class = OtpVerifySerializers

    def post(self,request):
        user_id = request.data['user_id']
        get_otp = request.data['otp']

        user = User.objects.filter(id=user_id).first()

        if user:
            if user.otp == get_otp:
                user_auth = authenticate(user)
                if user_auth:
                    return Response({
                        'id': user_auth.id,
                        'username': user_auth.username,
                        'email': user_auth.email,
                    })
                else:
                    return Response({
                        'Error':'Invalid credentials username or password didnt matched.'},
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
            else:
                return Response({
                    'otp':'otp didnot matched'
                })
        else:
            return Response(
                {'Error':'No such User Found'},
                status=status.HTTP_204_NO_CONTENT)
        

# search people 

class PeopleSearch(APIView):

    def get(self,request,*args, **kwargs):
        query = self.request.query_params.get('query')
        
        if query == None:
            query = ''

        if query:
            data = User.objects.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query)
            )
        
        else:
            data = User.objects.none()

        seriallizer = UserListSerializers(data, many=True)
        return Response(seriallizer.data)

