import os

from django import test
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from artitone.settings import BASE_DIR
from artworks.models import Artwork
from artworks.models import Category
from artworks.models import Picture
from profiles.models import Artist
from profiles.models import User
from profiles.models import UserType


class TestCase(test.TestCase):
    def setUp(self):
        super().setUp()
        self.admin = User.objects.create_superuser(email="admin@admin.com", password="admin")
        self.user = get_user_model().objects.create_user(
            email="vangogh@gmail.com",
            password="where_is_my_ear",
            type=UserType.ARTIST,
        )
        self.artist = Artist.objects.create(
            user=self.user,
            user_name="Van Gogh",
            first_name="Vincint",
            last_name="Gogh",
        )
        self.category = Category.objects.create(name="Painting")
        self.title = "Starry Night"
        self.price = 999.99
        self.texture = Artwork.SATIN
        self.content = "Starry starry night."

        self.picture = Picture.objects.create(
            picture=SimpleUploadedFile(
                name="test_images/test_artwork.png",
                content=open(
                    os.path.join(BASE_DIR, "static/test_images/test_artwork.png"), "rb"
                ).read(),
            )
        )
        self.artist.photo = self.picture
        self.artwork = Artwork.objects.create(
            artist=self.artist,
            title=self.title,
            category=self.category,
            price=self.price,
            texture=self.texture,
            content=self.content,
        )
        self.artwork.pictures.add(self.picture)
        self.artwork.tags.add("Minimalism")
        self.artwork.colors.add("#ffffff")

    def tearDown(self):
        super().tearDown()
        self.artwork.delete()
        self.picture.delete()
        self.artist.delete()
        self.category.delete()
