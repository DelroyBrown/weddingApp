# weddingApp_RSVP/forms.py
from django import forms
from .models import RSVP, Attendee
from django.forms import inlineformset_factory


class RSVPCreateForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = ["family_name", "email", "ceremony", "after_party", "zoom", "message"]


class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ["name", "dietary_restrictions"]


class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = ["response", "reason"]


AttendeeFormSet = inlineformset_factory(
    RSVP, Attendee, form=AttendeeForm, extra=5, can_delete=False
)
