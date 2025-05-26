# weddingApp_gallery\views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import PhotoUploadForm
from .models import Photo


def gallery_page(request):
    # Handle upload POST
    if request.method == "POST":
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("weddingApp_gallery:gallery")
    else:
        form = PhotoUploadForm()

    # Always show latest photos
    photos = Photo.objects.order_by("-uploaded_at")

    # AJAX Endpoint for auto refesh
    if request.GET.get("ajax"):
        data = [{"url": p.image.url, "uploader": p.attendee.name}]
        return JsonResponse({"photos": data})

    return render(
        request,
        "gallery/gallery.html",
        {
            "form": form,
            "photos": photos,
        },
    )
