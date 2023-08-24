from django import forms
from django.db import transaction

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
