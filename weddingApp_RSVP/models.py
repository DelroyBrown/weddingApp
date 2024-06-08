# weddingApp_RSVP/models.py
from django.db import models


class RSVP(models.Model):
    token = models.CharField(max_length=100, unique=True)
    family_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    response = models.CharField(
        max_length=10, choices=[("yes", "Yes"), ("no", "No")], blank=True, null=True
    )
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.family_name} - {self.email}"


class Attendee(models.Model):
    rsvp = models.ForeignKey(RSVP, related_name="attendees", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dietary_restrictions = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
