# weddingApp_RSVP/views.py
import random
import string
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from .models import RSVP, Attendee
from .forms import RSVPForm, RSVPCreateForm, AttendeeFormSet


def create_rsvp_view(request):
    if request.method == "POST":
        form = RSVPCreateForm(request.POST)
        formset = AttendeeFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            rsvp = form.save(commit=False)
            rsvp.token = generate_unique_token(rsvp.family_name)
            rsvp.save()
            formset.instance = rsvp
            formset.save()
            send_rsvp_email(rsvp)
            return render(request, "RSVP/rsvp_thank_you.html")
        else:
            print(form.errors)
            print(formset.errors)
    else:
        form = RSVPCreateForm()
        formset = AttendeeFormSet()

    return render(
        request, "RSVP/create_rsvp_form.html", {"form": form, "formset": formset}
    )


def generate_unique_token(family_name):
    cleaned_name = "".join(e for e in family_name if e.isalnum()).upper()
    random_chars = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    token = f"{cleaned_name}-{random_chars}"
    return token


def send_rsvp_email(rsvp):
    rsvp_link = f"http://localhost:8000/rsvp/{rsvp.token}/"
    subject = "You're invited to our wedding"
    message = f"Hello {rsvp.family_name},\n\nYou're invited to our wedding! Please RSVP using the following link: {rsvp_link}\n\nThank you!"
    send_mail(subject, message, "your_email@example.com", [rsvp.email])


def rsvp_view(request, token):
    rsvp = get_object_or_404(RSVP, token=token)

    if request.method == "POST":
        form = RSVPForm(request.POST, instance=rsvp)
        formset = AttendeeFormSet(request.POST, instance=rsvp)

        if form.is_valid() and formset.is_valid():
            rsvp = form.save()
            formset.save()
            return render(request, "RSVP/rsvp_thank_you.html")
    else:
        form = RSVPForm(instance=rsvp)
        formset = AttendeeFormSet(instance=rsvp)

    return render(request, "RSVP/rsvp_form.html", {"form": form, "formset": formset})


def rsvp_thank_you(request):
    return render(request, "RSVP/rsvp_thank_you.html")
