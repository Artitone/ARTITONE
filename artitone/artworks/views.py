import logging
import time

from artworks.forms import CreateArtworkForm, CustomPayPalPaymentsForm
from artworks.models import Artwork
from django.shortcuts import redirect, render
from django.urls import reverse

# from paypal.standard.forms import PayPalPaymentsForm
from profiles.models import Artist, ArtistPaymentMethod

logger = logging.getLogger("artitone")
# Create your views here.


def upload_artwork(request):
    """create a new Artwork and save it to the database."""
    user = request.user
    if not user.is_artist:
        return redirect("home")

    form = CreateArtworkForm(None)
    artist_profile = Artist.objects.get(pk=user)

    if request.method == "POST":
        post = request.POST.copy()
        post.update({"artist": artist_profile})
        request.POST = post

        form = CreateArtworkForm(request.POST, request.FILES)

        artwork = form.save(target_artist=artist_profile)
        if artwork:
            return redirect("artist_profile_page", pk=user.pk)

    return render(
        request,
        "artworks/upload_artworks.html",
        {"artwork_form": form, "artist": artist_profile},
    )


def delete_artwork(request, pk):
    user = request.user
    if not user.is_artist:
        return redirect("home")
    Artwork.objects.filter(pk=pk).delete()
    return redirect("artist_profile_page", pk=user.pk)


def purchase_artwork(request, pk, alert=None):
    user = request.user
    artist = Artist.objects.get(pk=user)
    artwork = Artwork.objects.get(pk=pk)
    payment_method = ArtistPaymentMethod.objects.get(pk=artist)

    # What you want the button to do.
    time_stamp = time.time()
    paypal_dict = {
        "business": payment_method.business_email,
        "amount": artwork.price,
        "item_name": artwork.title,
        "invoice": str(artist.pk) + str(artwork.pk) + str(time_stamp),
        "notify_url": request.build_absolute_uri(reverse("paypal-ipn")),
        "return": request.build_absolute_uri(
            reverse("purchase_success", kwargs={"pk": artwork.pk})
        ),
        "cancel_return": request.build_absolute_uri(
            reverse("purchase_fail", kwargs={"pk": artwork.pk})
        ),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = CustomPayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form, "alert": alert}
    return render(request, "payment.html", context)


def purchase_success(request, pk):
    return purchase_artwork(request, pk, "Successfully payed!!")


def purchase_fail(request, pk):
    return purchase_artwork(request, pk, "Payment failed!!")
