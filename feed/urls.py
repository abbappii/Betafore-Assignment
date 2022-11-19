
from django.urls import path , include
from .views import PostCreateViewset, Like_View
from rest_framework import routers

router = routers.DefaultRouter()
router.register('timeline-post',PostCreateViewset,basename='post')

urlpatterns = [ 
    path("",include(router.urls)),
]

urlpatterns_l_c = [
    path('post-like/', Like_View.as_view(),name='like'),

]

urlpatterns += urlpatterns_l_c