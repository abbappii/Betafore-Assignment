
from django.urls import path 
from .views import UserRegisterView, PeopleSearch, UserLoginOtpSendView, UserLoginOtpVerifyView

urlpatterns = [ 
    path('register/',UserRegisterView.as_view(),name='register'),
    path('user-search/',PeopleSearch.as_view(),name='user_search'),
    
    path('login-otp-send/', UserLoginOtpSendView.as_view(),name='login_otp_send'),
    path('verify-login-otp/', UserLoginOtpVerifyView.as_view(),name='verify_login_otp'),
]