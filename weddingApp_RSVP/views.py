# weddingApp_RSVP/views.py
import random
import string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.forms import modelformset_factory, inlineformset_factory
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render, get_object_or_404, redirect
from .models import RSVP, Attendee
from .forms import RSVPForm, RSVPCreateForm, AttendeeFormSet, AttendeeForm


def create_rsvp_view(request):
    if request.method == "POST":
        form = RSVPCreateForm(request.POST)
        formset = AttendeeFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            rsvp = form.save(commit=False)
            rsvp.token = generate_unique_token(rsvp.family_name)
            rsvp.save()

            # Save attendees without dietary info (this will be handled during RSVP)
            formset.instance = rsvp
            formset.save()

            # Send the email invite
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
    rsvp_link = f"https://kadel-6d5f7df9f1e4.herokuapp.com/rsvp/{rsvp.token}/"
    subject = "You're invited to our wedding"

    if rsvp.ceremony and rsvp.after_party:
        invitation_message = "You're invited to our wedding ceremony and after party!"
        event_location_message = "Everything will be held at: Crowne Plaza, Oxford Road, Beaconsfield, Gerrards Cross, HP9 2XE on June 7th 2025, 2:30pm. Please arrive for 2pm."
    elif rsvp.ceremony:
        invitation_message = "You're invited to the ceremony of our wedding!"
        event_location_message = "The ceremony will be held at: Crowne Plaza, Oxford Road, Beaconsfield, Gerrards Cross, HP9 2XE on June 7th 2025, 2:30pm. Please arrive for 2pm."
    elif rsvp.after_party:
        invitation_message = "You're invited to our wedding after party!"
        event_location_message = "The after party will be held at: Crowne Plaza, Oxford Road, Beaconsfield, Gerrards Cross, HP9 2XE on June 7th 2025, 7:30pm."
    else:
        invitation_message = (
            "You're invited to our wedding!"
        )
        event_location_message = ""

    attendees = rsvp.attendees.all()

    html_content = render_to_string(
        "RSVP/emails/invite_email.html",
        {
            "family_name": rsvp.family_name,
            "rsvp_link": rsvp_link,
            "invitation_message": invitation_message,
            "event_location_message": event_location_message,
            "message": rsvp.message,
            "attendees": attendees,
            "subject": subject,
        },
    )
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject, text_content, "delroybrown.db@gmail.com", [rsvp.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()




def rsvp_view(request, token):
    rsvp = get_object_or_404(RSVP, token=token)

    # Get the number of existing attendees
    existing_attendees_count = rsvp.attendees.count()

    # Create the formset with no extra forms (only show existing attendees)
    AttendeeFormSetLimited = inlineformset_factory(
        RSVP, Attendee, form=AttendeeForm, extra=0, can_delete=False
    )

    if request.method == "POST":
        form = RSVPForm(request.POST, instance=rsvp)
        formset = AttendeeFormSetLimited(request.POST, instance=rsvp)

        if form.is_valid() and formset.is_valid():
            rsvp = form.save()
            formset.save()

            send_rsvp_notification_email(rsvp)
            return redirect("weddingApp_RSVP:rsvp_thank_you")
        else:
            print("RSVP Form Errors:", form.errors)
            print("Formset Errors:", formset.errors)
    else:
        form = RSVPForm(instance=rsvp)
        # Render only the existing attendee forms
        formset = AttendeeFormSetLimited(instance=rsvp)

    return render(request, "RSVP/rsvp_form.html", {"form": form, "formset": formset})


def send_rsvp_notification_email(rsvp):
    subject = "New RSVP Submission: {} {}".format(rsvp.family_name, rsvp.email)
    from_email = settings.EMAIL_HOST_USER
    to_emails = [
        settings.EMAIL_HOST_USER,
        "delroybrown.db@gmail.com",
        "karissaprince@yahoo.co.uk",
    ]

    if rsvp.response == "yes":
        response_message = "I'll definitely be there, I can't wait!"
    else:
        response_message = "Sorry to miss it, but I won't be able to make it."

    attendees = rsvp.attendees.all()

    html_content = render_to_string(
        "RSVP/emails/rsvp_notification_email.html",
        {
            "rsvp": rsvp,
            "response_message": response_message,
            "attendees": attendees,
        },
    )
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
    email.attach_alternative(html_content, "text/html")
    email.send()


def rsvp_thank_you(request):
    return render(request, "RSVP/rsvp_response.html")
