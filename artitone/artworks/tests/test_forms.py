import os

from django.core.files.images import get_image_dimensions
from django.core.files.uploadedfile import SimpleUploadedFile

from artitone.settings import BASE_DIR
from artworks.forms import CreateArtworkForm
from artworks.models import Artwork
from artworks.tests.unittest_setup import TestCase


class CreateArtworkFormTest(TestCase):
    def test_validation(self):
        data = {
            "title": "Sunflower",
            "category": self.category,
            "price": 666.66,
            "content": "flowerrr!",
        }
        picture_1 = SimpleUploadedFile(
            name="test_images/test_artwork.png",
            content=open(
                os.path.join(BASE_DIR, "static/test_images/test_artwork.png"), "rb"
            ).read(),
        )

        form = CreateArtworkForm(data, {"picture_1": picture_1})
        self.assertIsNotNone(form.save(self.artist))
        posted_artwork = Artwork.objects.get(title="Sunflower")
        self.assertEqual(posted_artwork.title, "Sunflower")
        self.assertEqual(posted_artwork.category, self.category)
        self.assertEqual(posted_artwork.price, 666.66)
        self.assertEqual(
            get_image_dimensions(posted_artwork.pictures.all()[0].picture.file)[1], 500
        )
        self.assertEqual(posted_artwork.content, "flowerrr!")
