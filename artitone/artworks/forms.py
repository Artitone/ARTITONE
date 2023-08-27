import io
from PIL import Image
from rembg import remove

from django import forms
from django.db import transaction
from paypal.standard.forms import PayPalPaymentsForm

from artworks.models import Artwork


class CreateArtworkForm(forms.ModelForm):
    """This is the form used for creating a new post for volunteer gallery."""
    class Meta:
        model = Artwork
        fields = (
            "name",
            "photo",
            "category",
            "price",
            "content",
        )

    @transaction.atomic
    def save(self, target_artist):
        if self.is_valid():
            self.crop_image()
            return Artwork.objects.create(
                artist=target_artist,
                name=self.cleaned_data.get("name"),
                photo=self.cleaned_data.get("photo"),
                price=self.cleaned_data.get("price"),
                category=self.cleaned_data.get("category"),
                content=self.cleaned_data.get("content"),
            )
        return None
        
    def delete(self, post_pk):
        Artwork.objects.filter(pk=post_pk).delete()
    
    def get_image(self):
        return "test", self.files.get("photo").file.getvalue()
    
    def crop_image(self):
        im = Image.open(self.files.get("photo").file)
        im = remove(im)
        imgByteArr = io.BytesIO()
        im.save(imgByteArr, format='PNG')
        self.files.get("photo").file = imgByteArr


class CustomPayPalPaymentsForm(PayPalPaymentsForm):

    def get_html_submit_element(self):
        return """<button type="submit">Continue on PayPal website</button>"""