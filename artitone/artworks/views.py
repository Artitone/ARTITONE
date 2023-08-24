import boto3
import time  

from decimal import Decimal

from django.shortcuts import redirect
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse

from artworks.forms import CreateArtworkForm
from artworks.models import Artwork
from profiles.models import Artist
from profiles.models import ArtistPaymentMethod
from artworks.utils.rekognition import detect_labels


# Create your views here.


def upload_artwork(request):
    """create a new Artwork and save it to the database."""
    user = request.user
    if not user.is_artist:
        return redirect("home")
     
    artist_profile = Artist.objects.get(pk=user)

    if request.method == "POST":
        post = request.POST.copy()
        post.update({"artist": artist_profile})
        request.POST = post

        form = CreateArtworkForm(request.POST, request.FILES)
        content = {"artwork_form": form, "is_tag_phase": False}

        # if "tags" not in post:
        #     content["is_tag_phase"] = True
        #     content["tags"] = extract_tags_from_image(form)
        #     artwork = form.save(target_artist=artist_profile)
        #     content["artwork"] = artwork
        #     content["colors"] = artwork.get_dominant_color()
        #     return render(
        #         request,
        #         "artworks/upload_artworks.html",
        #         content,
        #     )
        # else:
        #     artwork_pk = post.getlist('artwork_pk')
        #     tags = post.getlist('tags')
        #     form.set_tags(artwork_pk, tags)

        #     return redirect("my_artworks", pk=user.pk)
        artwork = form.save(target_artist=artist_profile)
        texture, tags = extract_tags_from_image(form)
        colors = artwork.get_dominant_color()
        set_texture(artwork, texture)
        set_tags(artwork, tags)
        set_color(artwork, colors)
        return redirect("my_artworks", pk=user.pk)

    else:
        form = CreateArtworkForm()
        return render(
            request,
            "artworks/upload_artworks.html",
            {"artwork_form": form, "artist": artist_profile},
        )


def update_tags(request, pk):
    """update new Tags and save it to the database."""
    user = request.user
    if not user.is_artist:
        return redirect("home")
    if request.method == "POST":
        post = request.POST.copy()
        tags = post.getlist('tags')
        set_tags(pk, tags)

        return redirect("my_artworks", pk=user.pk)
    else:
        form = CreateArtworkForm()
        return render(
            request,
            "artworks/upload_artworks.html",
            {"artwork_form": form, "artist": artist_profile},
        )

def set_texture(artwork, texture):
    if texture == "Satin":
        artwork.texture = Artwork.SATIN
    elif texture == "Rough":
        artwork.texture = Artwork.ROUGH
    elif texture == "Matte":
        artwork.texture = Artwork.MATTE
    artwork.save()

def set_tags(artwork, tags):
    for tag in tags:
        artwork.tags.add(tag)

def set_color(artwork, colors):
    for color in colors:
        artwork.colors.add(color)


def extract_tags_from_image(form):
    image_name, bytes = form.get_image()
    texture, labels = detect_labels(bytes)

    return texture, labels
    # return ["label 1", "label 2", "label 3"]


def delete_artwork(request, pk):
    user = request.user
    if not user.is_artist:
        return redirect("home")
    Artwork.objects.filter(pk=pk).delete()
    return redirect("my_artworks", pk=user.pk)


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
        "item_name": artwork.name,
        "invoice": str(artist.pk)+str(artwork.pk)+str(time_stamp),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('purchase_success', kwargs={'pk':artwork.pk})),
        "cancel_return": request.build_absolute_uri(reverse('purchase_fail', kwargs={'pk':artwork.pk})),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form, "alert": alert}
    return render(request, "payment.html", context)


def purchase_success(request, pk):
    return purchase_artwork(request, pk, "Successfully payed!!")


def purchase_fail(request, pk):
    return purchase_artwork(request, pk, "Payment failed!!")