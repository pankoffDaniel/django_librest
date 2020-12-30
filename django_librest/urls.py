from django.contrib import admin
from django.urls import include, path

from django_librest.yasg import urlpatterns as doc_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api/v1/', include('apps.library.urls')),
]

urlpatterns += doc_urls
