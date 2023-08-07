from django import forms
from django.db import transaction

from artworks.models import Artwork


class CreateArtworkForm(forms.ModelForm):
    """This is the form used for creating a new post for volunteer gallery."""
    class Meta:
        model = Artwork
        fields = (
            "title",
            "photo",
            "category",
            "texture",
            "content",
        )

    @transaction.atomic
    def save(self, target_artist):
        if self.is_valid():
            return Artwork.objects.create(
                artist=target_artist,
                title=self.cleaned_data.get("title"),
                photo=self.cleaned_data.get("photo"),
                category=self.cleaned_data.get("category"),
                texture=self.cleaned_data.get("texture"),
                content=self.cleaned_data.get("content"),
            )
        return None
        
    def delete(self, post_pk):
        Artwork.objects.filter(pk=post_pk).delete()
    
    def get_image(self):
        return "test", self.files.get("photo").file.getvalue()

