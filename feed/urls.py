
from django.urls import path , include
from .views import PostCreateViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register('timeline-post',PostCreateViewset,basename='post')

urlpatterns = [ 
    path("",include(router.urls)),
]