import logging

from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from profiles.models import Artist
from profiles.models import User
from profiles.models import UserType


class ArtistCreationForm(UserCreationForm):
    name = forms.CharField(required=True)
    photo = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.type = UserType.ARTIST
        if commit:
            user.save()
            Artist.objects.create(
                user=user,
                name=self.cleaned_data.get("name"),
                photo=self.cleaned_data.get("photo"),
            )
        return user


class ArtistChangeForm(UserChangeForm):
    """This form is for edit Artist profile."""

    password = None

    class Meta(UserChangeForm.Meta):
        model = Artist
        fields = (
            "name",
            "website",
            "photo",
            "description",
        )

    @transaction.atomic
    def save(self, commit=True):
        user = self.instance
        artist = Artist.objects.get(pk=user)
        if self.is_valid():
            Artist.name = self.cleaned_data.get("name")
            Artist.photo = self.cleaned_data.get("photo")
            Artist.website = self.cleaned_data.get("website")
            Artist.description = self.cleaned_data.get("description")
            Artist.save()
        else:
            logger = logging.getLogger(__name__)
            logger.error(self.errors)
