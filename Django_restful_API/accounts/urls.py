from django.urls import path
from .views import RegisterApiView, LoginApiView, LogoutApiView

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register_api'),
    path('login/', LoginApiView.as_view(), name='login_api'),
    path('logout/', LogoutApiView.as_view(), name='logout_api'),
]