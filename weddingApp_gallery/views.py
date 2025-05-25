from django.shortcuts import render


def gallery_page(request):
    return render(request, "gallery/gallery.html")
