import os

from django import test
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from artitone.settings import BASE_DIR
from artworks.models import Artwork
from artworks.models import Category
from artworks.models import Picture
from profiles.models.artist import Artist
from profiles.models.user import User
from profiles.models.user import UserType


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
        self.category2 = Category.objects.create(name="Sculpture")
        self.category3 = Category.objects.create(name="Wall Arts")
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
        self.picture2 = Picture.objects.create(
            picture=SimpleUploadedFile(
                name="test_images/test_artwork_2.png",
                content=open(
                    os.path.join(BASE_DIR, "static/test_images/test_artwork_2.png"), "rb"
                ).read(),
            )
        )
        self.artist.photo = self.picture.picture

        self.artwork = Artwork.objects.create(
            artist=self.artist,
            title=self.title,
            category=self.category,
            price=self.price,
            texture=self.texture,
            content=self.content,
        )
        self.artwork.pictures.add(self.picture)
        self.artwork.tags.add("minimalism")
        self.artwork.colors.add("#ffffff")

        self.artwork2 = Artwork.objects.create(
            artist=self.artist,
            title="Artwork2",
            category=self.category2,
            price=self.price,
            texture=Artwork.MATTE,
            content="Lalalala",
        )
        self.artwork2.pictures.add(self.picture2)
        self.artwork2.tags.add("modern")
        self.artwork2.colors.add("#000000")

    def tearDown(self):
        super().tearDown()
        self.artwork.delete()
        self.picture.delete()
        self.artist.delete()
        self.category.delete()
