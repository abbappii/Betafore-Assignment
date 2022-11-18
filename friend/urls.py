from django.urls import path

from . import views

urlpatterns = [ 
    path('list/',views.Friend_list_view.as_view(),name='friend_list'),
]