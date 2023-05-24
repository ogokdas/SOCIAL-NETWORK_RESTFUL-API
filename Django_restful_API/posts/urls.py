from django.urls import path
from .views import PostApiView, PostDetailApiView, LikeApiView, PostDeleteApiView


urlpatterns = [
    path('posts', PostApiView.as_view(), name='post_api'),
    path('posts/<slug:slug>', PostDetailApiView.as_view(), name='postdetail_api'),
    path('posts/<slug:slug>:delete', PostDeleteApiView.as_view(), name='postdelete_api'),
    path('likes', LikeApiView.as_view(), name='likes_api')
]