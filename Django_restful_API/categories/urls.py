from django.urls import path
from .views import CategoryApiView, CategoriesApiView


urlpatterns = [
    path('categories/<slug:slug>', CategoryApiView.as_view(), name='category_api'),
    path('categories', CategoriesApiView.as_view(), name='categories_api'),
]