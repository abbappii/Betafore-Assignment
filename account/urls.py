
from django.urls import path 
from .views import UserRegisterView, PeopleSearch

urlpatterns = [ 
    path('register/',UserRegisterView.as_view(),name='register'),
    path('user-search/',PeopleSearch.as_view(),name='user_search'),

    
]