import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import RequestFactory
from django.urls import reverse

from artitone.settings import BASE_DIR
from artworks.models import Artwork
from artworks.models import Category
from artworks.tests.unittest_setup import TestCase
from artworks.views import upload_artwork
from artworks.views import delete_artwork


class ArtworksTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client.login(email="vangogh@gmail.com", password="where_is_my_ear")

    def test_upload_artwork_page_loads(self):
        response = self.client.get(reverse("upload_artwork"))
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get(reverse("upload_artwork"))
        self.assertNotEqual(response.status_code, 200)

    def test_upload_artwork(self):
        rf = RequestFactory()
        request = rf.post(
            "/artworks/upload_artwork",
            {
                "title": "Sunflower",
                "category": self.category.pk,
                "price": 666.66,
                "content": "flowerrr!",
            },
        )
        request.FILES["picture_1"] = SimpleUploadedFile(
            name="test_images/test_artwork.png",
            content=open(
                os.path.join(BASE_DIR, "static/test_images/test_artwork.png"), "rb"
            ).read(),
        )
        print(Category.objects.all())
        request.user = self.artist.user

        response = upload_artwork(request)
        self.assertIn(response.status_code, [200, 302])
        self.assertEqual(len(Artwork.objects.all()), 2)

    def test_delete_artwork(self):
        rf = RequestFactory().get(f"/{self.artwork.pk}/upload_artwork")
        rf.user = self.user
        delete_artwork(rf, self.artwork.pk)
        self.assertEqual(len(Artwork.objects.all()), 0)