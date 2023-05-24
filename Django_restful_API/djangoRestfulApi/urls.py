from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('categories.urls')),
    path('api/', include('posts.urls')),
    path('api/', include('profiles.urls')),
    path('api/', include('home.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)