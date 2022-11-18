from django.urls import path

from . import views

urlpatterns = [ 
    path('list/',views.Friend_list_view.as_view(),name='friend_list'),
    path('send-friend-request/', views.Friend_list_view.as_view(),name='send_friend_request'),
    
]