from django.test.client import RequestFactory
from django.urls import reverse

from profiles.tests.unittest_setup import TestCase
from profiles.views.customer import add_to_basket


class BasketTest(TestCase):
    def setUp(self):
        """Setting up"""
        super().setUp()
        self.client.login(email="picasso@gmail.com", password="p_i_c_a_s_s_o")

    def test_view_basket(self):
        response = self.client.get(reverse("basket", args=[self.customer.pk]))
        self.assertIn(response.status_code, [200, 302])
        artworks = response.context["page_obj"]
        self.assertEqual(len(artworks), 0)
        self.customer.basket.add(self.artwork)
        response = self.client.get(reverse("basket", args=[self.customer.pk]))
        self.assertIn(response.status_code, [200, 302])
        artworks = response.context["page_obj"]
        self.assertEqual(len(artworks), 1)

    def test_add_to_basket(self):
        self.assertEqual(self.customer.basket.all().count(), 0)
        response = self.client.get(reverse("add_to_basket", args=[self.artwork.pk]))
        self.assertIn(response.status_code, [200, 302])
        self.assertEqual(self.customer.basket.all().count(), 1)
