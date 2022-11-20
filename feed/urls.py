
from django.urls import path , include
from .views import PostOnTimeLineView,PostCreateViewset,Withdraw_like_view, Like_View, CommentView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('timeline-post',PostCreateViewset,basename='post')

urlpatterns = [ 
    path("",include(router.urls)),
]

urlpatterns_l_c = [
    path('post-like/', Like_View.as_view(),name='like'),
    path('post-comment/',CommentView.as_view(),name='comment'),
    path('post-like-withdraw/', Withdraw_like_view.as_view(),name='like_withdraw'),

    path('post-create/',PostOnTimeLineView.as_view(),name='post_create'),
]

urlpatterns += urlpatterns_l_c