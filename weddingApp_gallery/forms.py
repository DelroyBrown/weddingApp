from django import forms
from .models import Photo


class PhotoUploadForm(forms.ModelForm):
    name = forms.CharField(
        label="Your Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "e.g. John Smith",
            }
        ),
    )
    message = forms.CharField(
        label="Message",
        max_length=255,
        required=False,
        widget=forms.Textarea(
            attrs={"rows": 2, "placeholder": "Optional short message..."}
        ),
    )

    class Meta:
        model = Photo
        fields = ["name", "message", "image"]

    def clean_image(self):
        img = self.cleaned_data["image"]
        if img.size > 12 * 1024 * 1024:
            raise forms.ValidationError("Image file too large (max 5 MB).")
        if img.content_type not in ("image/jpeg", "image/png"):
            raise forms.ValidationError("Only JPEG & PNG allowed.")
        return img
