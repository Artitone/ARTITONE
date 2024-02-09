from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def photo_upload(request):
    if request.method == "POST":
        # Handle the uploaded file. You might want to save it or process it as required.
        # After handling the upload, redirect to shop_interface with a flag.
        return redirect(f"{reverse('shop_interface')}?uploaded=true")
    return render(request, "photo_upload.html")
