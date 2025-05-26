from django.contrib import admin
from django.utils.html import format_html
from .models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "attendee",  # who uploaded
        "uploaded_at",  # when
        "image_preview",  # thumbnail
    )
    list_filter = (
        "uploaded_at",
        "attendee__name",
    )
    search_fields = ("attendee__name",)
    readonly_fields = (
        "uploaded_at",
        "image_preview",
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width:150px; object-fit:cover;" />',
                obj.image.url,
            )
        return ""

    image_preview.short_description = "Preview"
