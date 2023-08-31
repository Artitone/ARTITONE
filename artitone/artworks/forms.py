import io
from PIL import Image
# from rembg import remove

from django import forms
from django.db import transaction
from paypal.standard.forms import PayPalPaymentsForm

from artworks.models import Artwork
from artworks.models import Picture
from artworks.models import file_size


class CreateArtworkForm(forms.ModelForm):
    """This is the form used for creating a new post for volunteer gallery."""
    picture_1 = forms.ImageField(required=True, validators=[file_size])
    picture_2 = forms.ImageField(required=False, validators=[file_size])
    picture_3 = forms.ImageField(required=False, validators=[file_size])
    picture_4 = forms.ImageField(required=False, validators=[file_size])
    class Meta:
        model = Artwork
        fields = (
            "name",
            "category",
            "price",
            "content",
        )

    @transaction.atomic
    def save(self, target_artist):
        if self.is_valid():
            # self.crop_image()
            picture_1 = Picture.objects.create(picture=self.cleaned_data.get("picture_1"))
            artwork = Artwork.objects.create(
                artist=target_artist,
                name=self.cleaned_data.get("name"),
                price=self.cleaned_data.get("price"),
                category=self.cleaned_data.get("category"),
                content=self.cleaned_data.get("content"),
            )
            artwork.pictures.add(picture_1)
            if self.cleaned_data['picture_2']:
                picture_2 = Picture.objects.create(picture=self.cleaned_data.get("picture_2"))
                artwork.pictures.add(picture_2)
            if self.cleaned_data['picture_3']:
                picture_3 = Picture.objects.create(picture=self.cleaned_data.get("picture_3"))
                artwork.pictures.add(picture_3)
            if self.cleaned_data['picture_4']:
                picture_4 = Picture.objects.create(picture=self.cleaned_data.get("picture_4"))
                artwork.pictures.add(picture_4)
        return artwork
        
    def delete(self, post_pk):
        Artwork.objects.filter(pk=post_pk).delete()
    
    def get_image(self):
        return "test", self.files.get("picture_1").file.getvalue()
    
    # def crop_image(self):
    #     im = Image.open(self.files.get("picture_1").file)
    #     im = remove(im)
    #     imgByteArr = io.BytesIO()
    #     im.save(imgByteArr, format='PNG')
    #     self.files.get("picture_1").file = imgByteArr


class CustomPayPalPaymentsForm(PayPalPaymentsForm):

    def get_html_submit_element(self):
        return """<button type="submit">Continue on PayPal website</button>"""