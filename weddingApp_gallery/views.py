# weddingApp_gallery\views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import PhotoUploadForm
from .models import Photo


def gallery_page(request):
    if request.method == "POST":
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("weddingApp_gallery:gallery")
    else:
        form = PhotoUploadForm()

    photos = Photo.objects.order_by("-uploaded_at")

    if request.GET.get("ajax"):
        data = [
            {"url": p.image.url, "name": p.name, "message": p.message} for p in photos
        ]
        return JsonResponse({"photos": data})

    return render(
        request,
        "gallery/gallery.html",
        {
            "form": form,
            "photos": photos,
        },
    )
