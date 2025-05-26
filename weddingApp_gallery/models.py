from django.db import models
from weddingApp_RSVP.models import Attendee


class Photo(models.Model):
    name = models.CharField(max_length=100, help_text="Your name (required)")
    message = models.CharField(
        max_length=255, blank=True, help_text="A short message (optional)"
    )
    image = models.ImageField(upload_to="gallery_photos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} @ {self.uploaded_at:%Y-%m-%d %H:%M}"
