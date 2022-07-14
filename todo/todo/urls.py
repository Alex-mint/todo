
from django.contrib import admin
from django.urls import path
from app.views import Home, generate_csrf

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('task/', Home.as_view(), name='task'),
    path('csrf/', generate_csrf),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
