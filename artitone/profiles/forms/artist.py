import logging

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from artitone.utils import resize_image
from profiles.models import Artist
from profiles.models import ArtistPaymentMethod
from profiles.models import User
from profiles.models import UserType

logger = logging.getLogger("artitone")


class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    email = UsernameField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "", "id": "login-email"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "id": "login-pwd",
            }
        )
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = authenticate(username=email, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError(
                "Sorry, that login was invalid. Please try again."
            )
        return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = authenticate(username=email, password=password)
        return user


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
        if self.cleaned_data.get("photo"):
            resize_image(self.cleaned_data.get("photo"), height=200, width=200)
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
