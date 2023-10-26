import os

from django.core.exceptions import ValidationError
from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

from profiles.models.artist import Artist

# Create your models here.


class Category(models.Model):
    """The Category type.

    Attributes:
        parent: parent Category, root Category is none.
        name: Category name.
    """

    parent = models.ForeignKey(
        "self", related_name="children", on_delete=models.CASCADE, blank=True, null=True
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


def file_size(value):  # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("File too large. Size should not exceed 2 MiB.")


def _post_photo_path(instance, filename):
    return f"artwork/{instance.artist.user.id}/{filename}"


def _post_picture_path(instance, filename):
    return f"artwork/{filename}"


def _post_3d_model_path(instance, filename):
    return f"3d_models/{filename}"


def validate_3d_model_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = [".skp", ".3dm"]
    if not ext.lower() in valid_extensions:
        raise ValidationError(f"Unsupported file extension: {ext.lower()}.")


class Picture(models.Model):
    picture = models.ImageField(
        upload_to=_post_picture_path, blank=True, null=True, validators=[file_size]
    )

    def __str__(self):
        return self.picture.url


class TaggedColors(TaggedItemBase):
    content_object = models.ForeignKey("Artwork", on_delete=models.CASCADE, null=True)


class TaggedCustom(TaggedItemBase):
    content_object = models.ForeignKey("Artwork", on_delete=models.CASCADE, null=True)


class IndustrialModel(models.Model):
    model = models.FileField(
        upload_to=_post_3d_model_path,
        blank=True,
        null=False,
        validators=[validate_3d_model_extension],
        help_text="Upload your 3d model files for better exposure chances.",
    )
    texture = models.ImageField(
        upload_to=_post_3d_model_path,
        blank=True,
        null=False,
        validators=[file_size],
        help_text="Upload your 3d model texture as well.",
    )

    def __str__(self):
        return str(self.artwork)


class Artwork(models.Model):
    """The Artwork type.

    Attributes:
        artist: The owner of the post. Posts appear on this volunteer's profile.
        name: post name.
        photo: post feature. Image field, required.
        tags: artwork tags, autogen+user add.
        content: post content.
    """

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, blank=False)
    title = models.CharField(
        max_length=200,
        help_text="Include keywords that buyers would use to search for your item.",
    )
    pictures = models.ManyToManyField(
        Picture,
        blank=True,
        related_name="pictures",
        help_text="Requirement:\n 1 on white background.",
    )
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    price = models.FloatField(default=0)
    SATIN = "SA"
    MATTE = "MA"
    ROUGH = "RO"
    TEXTURE_CHOICES = [
        (SATIN, "Satin"),
        (MATTE, "Matte"),
        (ROUGH, "Rough"),
    ]
    texture = models.CharField(max_length=2, choices=TEXTURE_CHOICES, blank=False, null=True)
    tags = TaggableManager(through=TaggedCustom, related_name="tags")
    colors = TaggableManager(through=TaggedColors, related_name="colors")
    content = models.TextField(help_text="Caption your artwork", default="")
    pubdate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    model = models.OneToOneField(IndustrialModel, null=True, blank=True, on_delete=models.CASCADE)

    PUBLISHED = "PU"
    IN_PROGRESS = "PR"
    ARCHIVED = "AR"
    STATUS_CHOICES = [
        (PUBLISHED, "Published"),
        (IN_PROGRESS, "In Progress"),
        (ARCHIVED, "Archived"),
    ]
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, blank=False, default=PUBLISHED)

    def __str__(self):
        return self.title
