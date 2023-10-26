from django.urls import reverse

from purchases.models.order import Order
from purchases.models.purchase import Purchase
from purchases.tests.unittest_setup import TestCase
from purchases.views import purchase_artwork
from purchases.views import purchase_success

# Create your tests here.


class TestPurchaseArtwork(TestCase):
    def setUp(self):
        super().setUp()
        self.client.login(email="picasso@gmail.com", password="p_i_c_a_s_s_o")

    def test_purchase_artwork(self):
        self.assertEqual(Order.objects.all().count(), 0)
        self.assertEqual(Purchase.objects.all().count(), 0)
        response = self.client.get(reverse("purchase_artwork", args=[self.artwork.pk]))
        self.assertIn(response.status_code, [200, 302])
        form = response.context["form"]
        self.assertEqual(form.initial["business"], self.payment.business_email)
        self.assertEqual(Order.objects.all().count(), 1)
        self.assertEqual(Purchase.objects.all().count(), 1)
        response = self.client.get(reverse("purchase_artwork", args=[self.artwork.pk]))
        self.assertIn(response.status_code, [200, 302])
        form = response.context["form"]
        self.assertEqual(form.initial["business"], self.payment.business_email)
        self.assertEqual(Order.objects.all().count(), 1)
        self.assertEqual(Purchase.objects.all().count(), 1)

    def test_purchase_success(self):
        self.order = Order.objects.create(customer=self.customer)
        self.purchase = Purchase.objects.create(
            order=self.order,
            artwork=self.artwork,
            price=self.artwork.price,
        )
        response = self.client.get(reverse("purchase_success", args=[self.order.id]))
        self.assertIn(response.status_code, [200, 302])
        self.assertEqual(Order.objects.all().count(), 1)
        self.assertEqual(Purchase.objects.all().count(), 1)
        self.order.delete()
        self.purchase.delete()

    def test_purchase_fail(self):
        self.order = Order.objects.create(customer=self.customer)
        self.purchase = Purchase.objects.create(
            order=self.order,
            artwork=self.artwork,
            price=self.artwork.price,
        )
        response = self.client.get(reverse("purchase_fail", args=[self.order.id]))
        self.assertIn(response.status_code, [200, 302])
        self.assertEqual(Order.objects.all().count(), 0)
        self.assertEqual(Purchase.objects.all().count(), 0)
