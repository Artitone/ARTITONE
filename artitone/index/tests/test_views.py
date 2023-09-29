import os

from django.contrib import auth
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import RequestFactory
from django.urls import reverse

from artitone.settings import BASE_DIR
from artworks.models import Picture
from index.tests.unittest_setup import TestCase
from index.views.home import home
from profiles.models.artist import Artist
from profiles.models.customer import Customer


class IndexTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client.login(email="vangogh@gmail.com", password="where_is_my_ear")

    def test_index(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_search_by_keyword(self):
        data = {}
        response = self.client.get(reverse("home"), data)
        artworks = response.context["page_obj"].object_list
        self.assertEqual(len(artworks), 2)

        data["keyword"] = "Artwork"
        response = self.client.get(reverse("home"), data)
        artworks = response.context["page_obj"].object_list
        self.assertEqual(len(artworks), 1)

        data["keyword"] = "lala"
        response = self.client.get(reverse("home"), data)
        artworks = response.context["page_obj"].object_list
        self.assertEqual(len(artworks), 1)

        data["keyword"] = "lalaLalala"
        response = self.client.get(reverse("home"), data)
        artworks = response.context["page_obj"].object_list
        self.assertEqual(len(artworks), 0)

    def test_search_by_tags(self):
        data = {}
        response = self.client.get(reverse("home"), data)
        artworks = response.context["page_obj"].object_list
        self.assertEqual(len(artworks), 2)

        data["keyword"] = "Minimalism"
        response = self.client.get(reverse("home"), data)
        artworks = response.context["page_obj"].object_list
        self.assertEqual(len(artworks), 1)

        data["keyword"] = "Minimalist"
        response = self.client.get(reverse("home"), data)
        artworks = response.context["page_obj"].object_list
        self.assertEqual(len(artworks), 0)

    def test_search_by_color_pallete(self):
        data = {}
        response = self.client.get(reverse("home"), data)
        artworks = response.context["page_obj"].object_list
        self.assertEqual(len(artworks), 2)

        data["color"] = "modern"
        response = self.client.get(reverse("home"), data)
        artworks = response.context["page_obj"].object_list
        self.assertEqual(len(artworks), 1)

        data["color"] = "contemporary"
        response = self.client.get(reverse("home"), data)
        artworks = response.context["page_obj"].object_list
        self.assertEqual(len(artworks), 0)

    def test_search_by_category(self):
        data = {}
        response = self.client.get(reverse("home"), data)
        artworks = response.context["page_obj"].object_list
        self.assertEqual(len(artworks), 2)

        data["category"] = "Sculpture"
        response = self.client.get(reverse("home"), data)
        artworks = response.context["page_obj"].object_list
        self.assertEqual(len(artworks), 1)

        data["category"] = "Wall Arts"
        response = self.client.get(reverse("home"), data)
        artworks = response.context["page_obj"].object_list
        self.assertEqual(len(artworks), 0)


class ProfileTest(TestCase):
    def setUp(self):
        super().setUp()

    def test_artist_login_popup(self):
        """Test artist login popups test if artist user can be logged in."""

        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)
        data = {
            "type": "login",
            "login-email": "vangogh@gmail.com",
            "login-password": "where_is_my_ear",
        }
        response = self.client.post(reverse("home"), data)
        self.assertIn(response.status_code, [200, 302])
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)

    def test_customer_login_popup(self):
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)
        data = {
            "type": "login",
            "login-email": "picasso@gmail.com",
            "login-password": "p_i_c_a_s_s_o",
        }
        response = self.client.post(reverse("home"), data)
        self.assertIn(response.status_code, [200, 302])
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)

    def test_artist_signup_popup(self):
        """Test artist signup popups, create an artist user,
        active it and test if it can be logged in."""

        artist_email = "davinci@gmail.com"
        artist_password = "can_you_draw_egg"
        artist_user_name = "davinci"
        artist_first_name = "Leonardo"
        artist_last_name = "Vinci"
        artist_website = "www.leo-vinci.com"
        artist_photo = Picture.objects.create(
            picture=SimpleUploadedFile(
                name="test_images/test_artwork.png",
                content=open(
                    os.path.join(BASE_DIR, "static/test_images/test_artwork.png"), "rb"
                ).read(),
            )
        )
        artist_paypal_email = "leovinci@gmail.com"
        data = {
            "type": "artist",
            "artist-email": artist_email,
            "artist-password1": artist_password,
            "artist-password2": artist_password,
            "artist-user_name": artist_user_name,
            "artist-first_name": artist_first_name,
            "artist-last_name": artist_last_name,
            "artist-website": artist_website,
            "artist-photo": artist_photo,
            "artist-paypal_email": artist_paypal_email,
        }
        _ = self.client.post(reverse("home"), data)
        self.assertEqual(Artist.objects.all().count(), 2)
        new_artist = Artist.objects.get(user_name=artist_user_name)
        self.assertEqual(new_artist.user.is_active, False)
        new_artist.user.is_active = True
        new_artist.user.save()
        data = {
            "type": "login",
            "login-email": artist_email,
            "login-password": artist_password,
        }
        _ = self.client.post(reverse("home"), data)
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)

    def test_customer_signup_popup(self):
        """Test costomer signup popups, create an customer user,
        active it and test if it can be logged in."""

        customer_email = "davinci@gmail.com"
        customer_password = "can_you_draw_egg"
        customer_user_name = "davinci"
        customer_first_name = "Leonardo"
        customer_last_name = "Vinci"
        customer_date_of_birth = "1999-02-07"
        customer_photo = Picture.objects.create(
            picture=SimpleUploadedFile(
                name="test_images/test_artwork.png",
                content=open(
                    os.path.join(BASE_DIR, "static/test_images/test_artwork.png"), "rb"
                ).read(),
            )
        )
        data = {
            "type": "customer",
            "customer-email": customer_email,
            "customer-password1": customer_password,
            "customer-password2": customer_password,
            "customer-user_name": customer_user_name,
            "customer-first_name": customer_first_name,
            "customer-last_name": customer_last_name,
            "customer-date_of_birth": customer_date_of_birth,
            "customer-photo": customer_photo,
        }
        _ = self.client.post(reverse("home"), data)
        self.assertEqual(Customer.objects.all().count(), 2)
        new_artist = Customer.objects.get(user_name=customer_user_name)
        self.assertEqual(new_artist.user.is_active, False)
        new_artist.user.is_active = True
        new_artist.user.save()
        data = {
            "type": "login",
            "login-email": customer_email,
            "login-password": customer_password,
        }
        _ = self.client.post(reverse("home"), data)
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
