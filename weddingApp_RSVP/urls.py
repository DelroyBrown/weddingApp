# weddingApp_RSVP/urls.py
from django.urls import path
from .views import rsvp_view, rsvp_thank_you, create_rsvp_view

app_name = "weddingApp_RSVP"

urlpatterns = [
    path("create/", create_rsvp_view, name="create_rsvp"),
    path("<str:token>/", rsvp_view, name="rsvp"),
    path("thank-you/", rsvp_thank_you, name="rsvp_thank_you"),
]
