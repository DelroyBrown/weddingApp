from django.db import models
from weddingApp_RSVP.models import Attendee


class Photo(models.Model):
    attendee = models.ForeignKey(
        Attendee,
        on_delete=models.CASCADE,
        help_text="Select the person who is uploading this photo",
    )
    image = models.ImageField(upload_to="gallery_photos/", help_text="JPEG/PNG Only")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attendee.name} @ {self.uploaded_at:%Y-%m-%d %H:%M}"
