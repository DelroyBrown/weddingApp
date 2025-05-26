from django import forms
from .models import Photo
from weddingApp_RSVP.models import Attendee


class PhotoUploadForm(forms.ModelForm):
    attendee = forms.ModelChoiceField(
        queryset=Attendee.objects.all().order_by("name"),
        empty_label="-- Select Your Name --",
        label="Your Name",
        help_text="If you don't see your name, you can not upload!",
    )

    class Meta:
        model = Photo
        fields = ["attendee", "image"]

    def clean_image(self):
        img = self.cleaned_data["image"]
        if img.size > 10 * 1024 * 1024:
            raise forms.ValidationError("Image size should be less than 5MB!")
        if not img.content_type in ("image/jpeg", "image/png"):
            raise forms.ValidationError("Only JPEG and PNG images are allowed!")
        return img
