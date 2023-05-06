from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('friends.urls')),
    path('api/', include('api.urls')),
]
