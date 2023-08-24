from artworks.utils.color_meter import _get_dominant_color
from django.core.exceptions import ValidationError
from django.db import models
from profiles.models import Artist
from taggit.managers import TaggableManager
from taggit.models import ItemBase, TaggedItemBase

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


class TaggedColors(TaggedItemBase):
    content_object = models.ForeignKey("Artwork", on_delete=models.CASCADE, null=True)

class TaggedCustom(TaggedItemBase):
    content_object = models.ForeignKey("Artwork", on_delete=models.CASCADE, null=True)


class Artwork(models.Model):
    """The Artwork type.

    Attributes:
        artist: The owner of the post. Posts appear on this volunteer's profile.
        title: post title.
        photo: post feature. Image field, required.
        tags: artwork tags, autogen+user add.
        content: post content.
    """

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, blank=False)
    name = models.CharField(max_length=200)
    photo = models.ImageField(
        upload_to=_post_photo_path, blank=True, null=True, validators=[file_size]
    )
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    price = models.FloatField(default=0)
    SATIN = "SA"
    MATTE = "MA"
    ROUGH = "RO"
    TEXTURE_CHOICES = [
        (SATIN, "Satin"),
        (MATTE, "Matte"),
        (ROUGH, "Rough"),
    ]
    texture = models.CharField(
        max_length=2, choices=TEXTURE_CHOICES, blank=False, null=True
    )
    tags = TaggableManager(through=TaggedCustom, related_name="tags")
    colors = TaggableManager(through=TaggedColors, related_name="colors")
    content = models.TextField(help_text="Caption your artwork", default="")

    def __str__(self):
        return self.title

    def get_dominant_color(self):
        return _get_dominant_color(self.photo.open())
        # or pass self.image.file, depending on your storage backend
        # We'll implement _get_dominant_color() below later
