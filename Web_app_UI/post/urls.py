from django.urls import path
from .import views

urlpatterns = [
    path("post", views.post_request, name="post"),
    path("post/<slug:slug>", views.post_details, name="details")
]