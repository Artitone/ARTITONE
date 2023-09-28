from django.db import models

from artworks.models import Artwork
from profiles.models.user import User
from profiles.models.user import _profile_photo_path


class Customer(models.Model):
    """The Customer profile type.

    Attributes:
        user: the one-to-one mapping of an authenticated user.
        first_name: the name given to an individual (often referred to as the
            first name in English speaking countries).
        last_name: the family name of an individual (often referred to as the
            last name in English speaking countries).
        date_of_birth: the birth date of an individual.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    user_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to=_profile_photo_path, blank=True, null=True)
    description = models.TextField(help_text="Introduce yourself here.", default="")
    basket = models.ManyToManyField(Artwork, blank=True, null=True)

    def __str__(self):
        return self.user_name

    @property
    def name(self):
        """Returns the full name of the volunteer."""
        return f"{self.first_name} {self.last_name}"