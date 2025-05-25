# weddingApp_base/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


app_name = "weddingApp_base"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("rsvp/", include("weddingApp_RSVP.urls", namespace="weddingApp_RSVP")),
    path('', include('weddingApp_home.urls')),
    path('gallery/', include('weddingApp_gallery.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
