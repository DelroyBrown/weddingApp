# weddingApp_gallery\urls.py
from django.urls import path
from .views import gallery_page
from django.conf import settings
from django.conf.urls.static import static


app_name = "weddingApp_gallery"


urlpatterns = [
    path('', gallery_page, name='gallery'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
