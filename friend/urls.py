from django.urls import path

from . import views

urlpatterns = [ 
    path('list/',views.Friend_list_view.as_view(),name='friend_list'),
    path('send-friend-request/', views.SendFriendRequests.as_view(),name='send_friend_request'),
    path('accept-friend-request/', views.Accept_frined_request.as_view(),name='accept_friend_request'),
    path('decline-friend-request/', views.DeclineFriendRequestView.as_view(),name='decline_friend_request'),
]