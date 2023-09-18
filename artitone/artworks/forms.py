import io
import logging

from artworks.models import Artwork, Picture, file_size
from artworks.utils.clip import clip_predict_label
from artworks.utils.color_meter import _get_dominant_color
from django import forms
from django.db import transaction
from paypal.standard.forms import PayPalPaymentsForm

# from rembg import remove
from PIL import Image

from artitone.utils import resize_image

logger = logging.getLogger("artitone")


class CreateArtworkForm(forms.ModelForm):
    """This is the form used for creating a new post for volunteer gallery."""

    picture_1 = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={"class": "artitone-image-upload form-control"}
        ),
        required=True,
        validators=[file_size],
    )
    picture_2 = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={"class": "artitone-image-upload form-control"}
        ),
        required=False,
        validators=[file_size],
    )
    picture_3 = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={"class": "artitone-image-upload form-control"}
        ),
        required=False,
        validators=[file_size],
    )
    picture_4 = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={"class": "artitone-image-upload form-control"}
        ),
        required=False,
        validators=[file_size],
    )

    class Meta:
        model = Artwork
        fields = (
            "title",
            "category",
            "price",
            "content",
        )
        widgets = {
            "category": forms.Select(
                attrs={"class": "form-control artitone-profile-select"}
            ),
            "price": forms.NumberInput(
                attrs={"class": "artitone-artworks-price", "min": 0}
            ),
            "content": forms.Textarea(
                attrs={"class": "form-control artitone-artworks-content"}
            ),
        }

    @transaction.atomic
    def save(self, target_artist):
        if self.is_valid():
            resize_image(self.cleaned_data.get("picture_1"), height=500)
            texture, tags = self.extract_tags_from_image()
            colors = self.get_dominant_color()

            picture_1 = Picture.objects.create(
                picture=self.cleaned_data.get("picture_1")
            )
            artwork = Artwork.objects.create(
                artist=target_artist,
                title=self.cleaned_data.get("title"),
                price=self.cleaned_data.get("price"),
                category=self.cleaned_data.get("category"),
                content=self.cleaned_data.get("content"),
            )
            artwork.pictures.add(picture_1)
            if self.cleaned_data["picture_2"]:
                resize_image(self.cleaned_data.get("picture_2"), height=500)
                picture_2 = Picture.objects.create(
                    picture=self.cleaned_data.get("picture_2")
                )
                artwork.pictures.add(picture_2)
            if self.cleaned_data["picture_3"]:
                resize_image(self.cleaned_data.get("picture_3"), height=500)
                picture_3 = Picture.objects.create(
                    picture=self.cleaned_data.get("picture_3")
                )
                artwork.pictures.add(picture_3)
            if self.cleaned_data["picture_4"]:
                resize_image(self.cleaned_data.get("picture_4"), height=500)
                picture_4 = Picture.objects.create(
                    picture=self.cleaned_data.get("picture_4")
                )
                artwork.pictures.add(picture_4)

            set_texture(artwork, texture)
            set_tags(artwork, tags)
            set_color(artwork, colors)

            return artwork
        else:
            logger.error(self.errors.as_data())
            return None

    def delete(self, post_pk):
        Artwork.objects.filter(pk=post_pk).delete()

    def get_image(self):
        return "test", self.files.get("picture_1").file.getvalue()

    def extract_tags_from_image(self):
        image = self.files.get("picture_1").file.getvalue()
        # image = self.cleaned_data.get("picture_1")
        with Image.open(io.BytesIO(image)) as im:
            texture, tags = clip_predict_label(im)
            # tags = clip_predict_tags(im)
        # texture, labels = detect_labels(bytes)

        # return texture, labels
        return texture, tags

    def get_dominant_color(self):
        image = self.cleaned_data.get("picture_1")
        return _get_dominant_color(image)


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


class CustomPayPalPaymentsForm(PayPalPaymentsForm):
    def get_html_submit_element(self):
        return """<button type="submit">Continue on PayPal website</button>"""
