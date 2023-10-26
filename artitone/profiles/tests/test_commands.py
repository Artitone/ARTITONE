from io import StringIO
import random
import string

from django.core.management import call_command
from django.test import TestCase

from profiles.models.artist import Artist
from profiles.models.customer import Customer
from profiles.models.user import User
from profiles.models.user import UserType


class TestCreateSuperUser(TestCase):
    def setUp(self):
        super().setUp()
        self.email = "super@admin.com"
        self.password = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def test_create_super_user(self):
        out = StringIO()
        call_command("add_default_user", email=self.email, password=self.password, stdout=out)
        self.assertTrue(User.objects.filter(email=self.email).exists())

    def test_already_exists(self):
        User.objects.create_superuser(
            email=self.email,
            password=self.password,
            is_active=True,
            type=UserType.ADMIN,
        )
        out = StringIO()
        call_command("add_default_user", email=self.email, password=self.password, stdout=out)
        self.assertIn("already exists", out.getvalue())

    def test_default_email(self):
        out = StringIO()
        call_command("add_default_user", stdout=out)
        self.assertFalse(User.objects.filter(email=self.email).exists())
        self.assertTrue(User.objects.filter(email="admin@admin.com").exists())


class TestAddTestUser(TestCase):
    def setUp(self):
        super().setUp()
        self.artist_email = "dif-axayasu61829476@hotmail.com"
        self.customer_email = "tamra_montoya32182948@outlook.com"
        self.password = "test1_Test2_test3"

    def test_create_test_user(self):
        out = StringIO()
        call_command("add_test_user", stdout=out)
        self.assertTrue(Artist.objects.filter(user_name="test_artist").exists())
        self.assertTrue(Customer.objects.filter(user_name="test_customer").exists())

    def test_already_exists(self):
        Artist.objects.create(
            user=User.objects.create_user(
                email=self.artist_email,
                password=self.password,
                is_active=True,
                type=UserType.ARTIST,
            ),
            user_name="test_artist",
        )
        Customer.objects.create(
            user=User.objects.create_user(
                email=self.customer_email,
                password=self.password,
                is_active=True,
                type=UserType.CUSTOMER,
            ),
            user_name="test_customer",
        )
        out = StringIO()
        call_command("add_test_user", stdout=out)
        self.assertIn("Test artist with email address already exists.", out.getvalue())
        self.assertIn("Test customer with email address already exists.", out.getvalue())
