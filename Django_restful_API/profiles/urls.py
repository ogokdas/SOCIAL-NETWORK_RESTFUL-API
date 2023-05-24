from django.urls import path
from .views import ProfileApiView, ProfileDetailApiView, ProfileSettingApiView, ProfileSearchApiView


urlpatterns = [
    path("profiles", ProfileApiView.as_view(), name="profile_api"),
    path("profiles/<slug:slug>", ProfileDetailApiView.as_view(), name="profiledetail_api"),
    path("profiles:setting", ProfileSettingApiView.as_view(), name="setting_api"),
    path("profiles:search", ProfileSearchApiView.as_view(), name="search_api")
]