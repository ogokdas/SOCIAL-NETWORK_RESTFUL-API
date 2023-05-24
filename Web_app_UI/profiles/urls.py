from django.urls import path
from .import views

urlpatterns = [
    path("profile", views.profile_request, name="profile"),
    path("profiledetail/<slug:slug>", views.profiledetail_request, name="profiledetail"),
    path("settings", views.settings_request, name="settings")
]