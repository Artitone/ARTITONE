from datetime import timedelta

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserType(models.IntegerChoices):
    """Container for all possible user types."""

    ADMIN = 0, "Admin"
    ARTIST = 1, "Artist"
    CUSTOMER = 2, "Customer"


class UserManager(BaseUserManager):
    """UserManager allows the app to override the required username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("creating a user requires an email field")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Creates and ordinary, everyday non-super user."""
        extra_fields["is_staff"] = False
        extra_fields["is_superuser"] = False
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Creates an Admin superuser."""
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["type"] = UserType.ADMIN

        if extra_fields.get("is_staff") is not True:
            raise ValueError("a superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("a superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """A User represents an abstract authenticated entity.

    Each user is associated with a particular Profile type
    (Artist|Customer) granting authorization to claim,
    modify, and delete the associated profile.

    Attributes:
        email: the unique email address associated with a particular user.
        password: the secret password to use during authentication.
    """

    username = None
    email = models.EmailField(
        verbose_name="email address",
        max_length=254,
        unique=True,
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    type = models.IntegerField(choices=UserType.choices)
    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    @property
    def is_artist(self):
        """Returns true if this user is associated with an artist."""
        return self.type == UserType.ARTIST

    @property
    def is_customer(self):
        """Returns true if this user is associated with an customer."""
        return self.type == UserType.CUSTOMER

    @property
    def is_admin(self):
        """Returns true if this user is an admin."""
        return self.type == UserType.ADMIN


def _profile_photo_path(instance, filename):
    if instance.user.is_artist:
        prefix = "artists"
    elif instance.user.is_customer:
        prefix = "customers"
    elif instance.user.is_admin:
        prefix = "admins"
    else:
        raise ValueError(f"unsupported user type {instance.user.type}")
    return f"{prefix}/{instance.user.id}/{filename}"


class Artist(models.Model):
    """The Artist profile type.

    Attributes:
        user: the one-to-one mapping of an authenticated user.
        name: the official name of the artist.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    user_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    photo = models.ImageField(upload_to=_profile_photo_path, blank=True, null=True)
    website = models.CharField(max_length=200, default="")
    description = models.TextField(help_text="Introduce your self/artwork here", default="", blank=True, null=True)

    def __str__(self):
        return self.user_name


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
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to=_profile_photo_path, blank=True, null=True)
    description = models.TextField(help_text="Introduce yourself here.", default="")

    def __str__(self):
        return self.user_name

    @property
    def name(self):
        """Returns the full name of the volunteer."""
        return f"{self.first_name} {self.last_name}"


class ArtistPaymentMethod(models.Model):
    """The ArtistPaymentMethod type.

    Attributes:
        user: the one-to-one mapping of an authenticated user.
        first_name: the name given to an individual (often referred to as the
            first name in English speaking countries).
        last_name: the family name of an individual (often referred to as the
            last name in English speaking countries).
        date_of_birth: the birth date of an individual.
    """

    artist = models.OneToOneField(
        Artist,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    business_email = models.EmailField(max_length=254)

