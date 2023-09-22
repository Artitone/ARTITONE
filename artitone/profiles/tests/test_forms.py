import os

from django.core.files.uploadedfile import SimpleUploadedFile

from artitone.settings import BASE_DIR
from profiles.forms.artist import ArtistChangeForm
from profiles.models import ArtistPaymentMethod
from profiles.tests.unittest_setup import TestCase


class ArtistChangeFormTest(TestCase):
    def setUp(self):
        super().setUp()
        self.photo = SimpleUploadedFile(
            name="test_images/test_artwork_2.png",
            content=open(
                os.path.join(BASE_DIR, "static/test_images/test_artwork_2.png"), "rb"
            ).read(),
        )

        self.data = {
            "user_name": "Paul Gauguin",
            "first_name": "Paul",
            "last_name": "Gauguin",
            "website": "www.PGauguin.com",
            "description": "PG in da house!",
            "paypal_email": "gauguin@paul.com",
        }

    def test_artist_change_form(self):
        self.assertEqual(self.artist.user_name, "Van Gogh")
        self.assertEqual(self.artist.first_name, "Vincint")
        self.assertEqual(self.artist.last_name, "Gogh")
        self.assertEqual(self.artist.photo, self.picture.picture)
        payment = ArtistPaymentMethod.objects.get(artist=self.artist)
        self.assertEqual(payment.business_email, "gogh@vincent.com")
        form = ArtistChangeForm(self.data, {"photo": self.photo}, instance=self.artist)
        form.save()
        self.assertEqual(self.artist.user_name, "Paul Gauguin")
        self.assertEqual(self.artist.first_name, "Paul")
        self.assertEqual(self.artist.last_name, "Gauguin")
        self.assertEqual(self.artist.photo, self.photo)
        payment = ArtistPaymentMethod.objects.get(artist=self.artist)
        self.assertEqual(payment.business_email, "gauguin@paul.com")
