import logging

from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from artworks.forms import CreateArtworkForm
from artworks.forms import CreateIndustrialModelForm
from artworks.models import Artwork

# from paypal.standard.forms import PayPalPaymentsForm
from profiles.models.artist import Artist

from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)
# Create your views here.


def upload_artwork(request):
    """create a new Artwork and save it to the database."""
    user = request.user
    if user.is_anonymous or not user.is_artist:
        return redirect("home")

    form = CreateArtworkForm(None)
    model_form = CreateIndustrialModelForm(None)
    artist_profile = Artist.objects.get(pk=user)

    if request.method == "POST":
        post = request.POST.copy()
        post.update({"artist": artist_profile})
        request.POST = post

        logger.debug(
            f"""\n==============UPLOAD_ARTWORK==============\n
            {request.POST}\n{request.FILES}\n
            ========================================"""
        )
        model_form = CreateIndustrialModelForm(request.POST, request.FILES)
        form = CreateArtworkForm(request.POST, request.FILES)

        artwork = form.save(target_artist=artist_profile)

        if artwork:
            model = model_form.save(artwork_pk=artwork.pk)
            logger.critical(
                f"""\n==============3D_MODEL==============\n
                {model}\n
                ========================================"""
            )
            return redirect("artist_profile_page", pk=user.pk)

    return render(
        request,
        "artworks/upload_artworks.html",
        {
            "artwork_form": form,
            "model_form": model_form,
            "artist": artist_profile,
        },
    )


def delete_artwork(request, pk):
    user = request.user
    if not user.is_artist:
        return redirect("home")
    artworks = Artwork.objects.filter(pk=pk)
    for artwork in artworks:
        if artwork.artist == Artist.objects.get(pk=user):
            artwork.delete()
    return redirect("artist_profile_page", pk=user.pk)
