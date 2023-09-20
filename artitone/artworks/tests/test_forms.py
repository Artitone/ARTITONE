import os

from django.core.files.images import get_image_dimensions
from django.core.files.uploadedfile import SimpleUploadedFile

from artitone.settings import BASE_DIR
from artworks.forms import CreateArtworkForm
from artworks.models import Artwork
from artworks.tests.unittest_setup import TestCase


class CreateArtworkFormTest(TestCase):
    """
    Test cases for CreateArtworkForm.
    """

    def setUp(self):
        super().setUp()
        self.picture_1 = SimpleUploadedFile(
            name="test_images/test_artwork.png",
            content=open(
                os.path.join(BASE_DIR, "static/test_images/test_artwork.png"), "rb"
            ).read(),
        )
        self.picture_2 = SimpleUploadedFile(
            name="test_images/test_artwork_2.png",
            content=open(
                os.path.join(BASE_DIR, "static/test_images/test_artwork_2.png"), "rb"
            ).read(),
        )
        self.picture_3 = SimpleUploadedFile(
            name="test_images/test_artwork_3.png",
            content=open(
                os.path.join(BASE_DIR, "static/test_images/test_artwork_3.png"), "rb"
            ).read(),
        )
        self.picture_4 = SimpleUploadedFile(
            name="test_images/test_artwork_4.png",
            content=open(
                os.path.join(BASE_DIR, "static/test_images/test_artwork_4.png"), "rb"
            ).read(),
        )
        self.data = {
            "title": "TestArt",
            "category": self.category,
            "price": 666.66,
            "content": "Test!",
        }

    def test_validation_matte(self):
        form = CreateArtworkForm(
            self.data,
            {
                "picture_1": self.picture_1,
                "picture_2": self.picture_2,
                "picture_3": self.picture_3,
                "picture_4": self.picture_4,
            },
        )
        self.assertIsNotNone(form.save(self.artist))
        posted_artwork = Artwork.objects.get(title="TestArt")
        self.assertEqual(posted_artwork.title, "TestArt")
        self.assertEqual(posted_artwork.texture, Artwork.MATTE)
        self.assertEqual(posted_artwork.category, self.category)
        self.assertEqual(posted_artwork.price, 666.66)
        self.assertEqual(
            get_image_dimensions(posted_artwork.pictures.all()[0].picture.file)[1], 500
        )
        self.assertEqual(posted_artwork.content, "Test!")

    def test_validation_satin(self):
        form = CreateArtworkForm(self.data, {"picture_1": self.picture_3})
        self.assertIsNotNone(form.save(self.artist))
        posted_artwork = Artwork.objects.get(title="TestArt")
        self.assertEqual(posted_artwork.title, "TestArt")
        self.assertEqual(posted_artwork.texture, Artwork.SATIN)

    def test_validation_rough(self):
        form = CreateArtworkForm(self.data, {"picture_1": self.picture_2})
        self.assertIsNotNone(form.save(self.artist))
        posted_artwork = Artwork.objects.get(title="TestArt")
        self.assertEqual(posted_artwork.title, "TestArt")
        self.assertEqual(posted_artwork.texture, Artwork.ROUGH)

    def test_delete(self):
        form = CreateArtworkForm(self.data, {"picture_1": self.picture_1})
        self.assertIsNotNone(form.save(self.artist))
        posted_artwork = Artwork.objects.get(title="TestArt")
        self.assertEqual(posted_artwork.title, "TestArt")
        self.assertIsNone(form.delete(posted_artwork.pk))
        self.assertFalse(Artwork.objects.filter(title="TestArt").exists())
