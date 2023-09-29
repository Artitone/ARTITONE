import os

from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from artitone.settings import BASE_DIR
from artworks.models import Picture
from profiles.models.artist import Artist
from profiles.models.user import User
from profiles.tests.unittest_setup import TestCase


class activateEmailTest(TestCase):
    """Test cases for Email Verification"""

    def setUp(self):
        """Setting up"""
        super().setUp()
        self.artist_email = "davinci@gmail.com"
        self.artist_password = "can_you_draw_egg"
        self.artist_user_name = "davinci"
        self.artist_first_name = "Leonardo"
        self.artist_last_name = "Vinci"
        self.artist_website = "www.leo-vinci.com"
        self.artist_photo = Picture.objects.create(
            picture=SimpleUploadedFile(
                name="test_images/test_artwork.png",
                content=open(
                    os.path.join(BASE_DIR, "static/test_images/test_artwork.png"), "rb"
                ).read(),
            )
        )
        self.artist_paypal_email = "leovinci@gmail.com"
        self.data = {
            "type": "artist",
            "artist-email": self.artist_email,
            "artist-password1": self.artist_password,
            "artist-password2": self.artist_password,
            "artist-user_name": self.artist_user_name,
            "artist-first_name": self.artist_first_name,
            "artist-last_name": self.artist_last_name,
            "artist-website": self.artist_website,
            "artist-photo": self.artist_photo,
            "artist-paypal_email": self.artist_paypal_email,
        }

    def test_user_inactive(self):
        """Assert User is inactive after sign up"""
        _ = self.client.post(reverse("home"), self.data)
        self.assertEqual(Artist.objects.all().count(), 2)
        new_artist = Artist.objects.get(user_name=self.artist_user_name)
        self.assertEqual(new_artist.user.is_active, False)

    def test_email_sent(self):
        _ = self.client.post(reverse("home"), self.data)
        test_user = User.objects.get(email=self.artist_email)
        uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
        token = default_token_generator.make_token(test_user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.artist_email])
        self.assertIn("Account Activation", mail.outbox[0].subject)
        self.assertIn(
            "Kindly click below given link to confirm your registration, ",
            mail.outbox[0].body,
        )
        self.assertIn(
            reverse("activate", args=[uidb64, token]),
            mail.outbox[0].body,
        )
