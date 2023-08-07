import boto3

from django.shortcuts import redirect
from django.shortcuts import render

from artworks.forms import CreateArtworkForm
from artworks.models import Artwork
from profiles.models import Artist
from artworks.utils.rekognition import detect_labels

# Create your views here.


def upload_artwork_image(request):
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

        if "tags" not in post:
            content["is_tag_phase"] = True
            content["tags"] = extract_tags_from_image(form)
            artwork = form.save(target_artist=artist_profile)
            content["artwork"] = artwork
            content["colors"] = artwork.get_dominant_color()
            return render(
                request,
                "artworks/upload_artworks.html",
                content,
            )
        else:
            artwork_pk = post.getlist('artwork_pk')
            tags = post.getlist('tags')
            form.set_tags(artwork_pk, tags)

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


def set_tags(pk, tags):
    artwork = Artwork.objects.get(pk=pk)
    for tag in tags:
        artwork.tags.add(tag)


def extract_tags_from_image(form):
    image_name, bytes = form.get_image()
    labels = detect_labels(image_name, bytes)

    return labels


def delete_artwork(request, pk):
    user = request.user
    if not user.is_artist:
        return redirect("home")
    Artwork.objects.filter(pk=pk).delete()
    return redirect("my_artworks", pk=user.pk)