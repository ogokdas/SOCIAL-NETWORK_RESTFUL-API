from django.urls import path
from . import views

urlpatterns = [
    path("category/<slug:slug>", views.categories, name="categories")
]