# weddingApp_RSVP/admin.py
from django.contrib import admin
from .models import RSVP, Attendee


class AttendeeInline(admin.TabularInline):
    model = Attendee
    extra = 1


class RSVPAdmin(admin.ModelAdmin):
    list_display = (
        "family_name",
        "email",
        "response",
        "created_at",
        "updated_at",
    )
    search_fields = ("family_name", "email")
    list_filter = ("response", "created_at")
    inlines = [AttendeeInline]


admin.site.register(RSVP, RSVPAdmin)
admin.site.register(Attendee)
