from django.urls import path
from .views import HomeApiView
#from .views import PostApiView, PostDetailApiView, LikeApiView, PostDeleteApiView, HomeApiView

urlpatterns = [
    path("", HomeApiView.as_view(), name="home_api"),
    path("home", HomeApiView.as_view(), name="home_")
]