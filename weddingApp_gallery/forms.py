# weddingApp_gallery/forms.py
from django import forms
from .models import Photo
from weddingApp_RSVP.models import Attendee


class PhotoUploadForm(forms.ModelForm):
    attendee = forms.ModelChoiceField(
        queryset=Attendee.objects.none(),  # placeholder
        empty_label="-- Select your RSVP & name --",
        label="Your RSVP & Name",
        help_text="If you don’t see your family or name, you can’t upload.",
    )

    class Meta:
        model = Photo
        fields = ["attendee", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        qs = Attendee.objects.select_related("rsvp").order_by(
            "rsvp__family_name", "name"
        )
        field = self.fields["attendee"]
        field.queryset = qs
        field.label_from_instance = lambda obj: f"{obj.rsvp.family_name} – {obj.name}"

    def clean_image(self):
        img = self.cleaned_data["image"]
        if img.size > 12 * 1024 * 1024:
            raise forms.ValidationError("Image file too large (max 12 MB).")
        if img.content_type not in ("image/jpeg", "image/png"):
            raise forms.ValidationError("Only JPEG and PNG files are allowed.")
        return img
