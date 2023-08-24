import logging

from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from profiles.models import Artist
from profiles.models import ArtistPaymentMethod
from profiles.models import User
from profiles.models import UserType


class ArtistCreationForm(UserCreationForm):
    user_name = forms.CharField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    website = forms.CharField(required=False)
    photo = forms.ImageField(required=False)
    paypal_email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.type = UserType.ARTIST
        if commit:
            user.save()
            artist = Artist.objects.create(
                user=user,
                user_name=self.cleaned_data.get("user_name"),
                first_name=self.cleaned_data.get("first_name"),
                last_name=self.cleaned_data.get("last_name"),
                photo=self.cleaned_data.get("photo"),
                website=self.cleaned_data.get("website"),
            )
            ArtistPaymentMethod.objects.create(
                artist=artist,
                business_email=self.cleaned_data.get("paypal_email"),
            )
        return user


class ArtistChangeForm(UserChangeForm):
    """This form is for edit Artist profile."""

    password = None

    class Meta(UserChangeForm.Meta):
        model = Artist
        fields = (
            "user_name",
            "first_name",
            "last_name",
            "photo",
            "website",
            "description",
        )

    @transaction.atomic
    def save(self, commit=True):
        user = self.instance
        artist = Artist.objects.get(pk=user)
        if self.is_valid():
            artist.user_name = self.cleaned_data.get("user_name")
            artist.first_name = self.cleaned_data.get("first_name")
            artist.last_name = self.cleaned_data.get("last_name")
            artist.photo = self.cleaned_data.get("photo")
            artist.website = self.cleaned_data.get("website")
            artist.description = self.cleaned_data.get("description")
            artist.save()
        else:
            logger = logging.getLogger(__name__)
            logger.error(self.errors)
