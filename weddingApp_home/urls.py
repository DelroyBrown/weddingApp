# weddingApp_base/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = "weddingApp_home"


urlpatterns = [
    path("", views.home, name="home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
