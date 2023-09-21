from profiles.tests.unittest_setup import TestCase
from profiles.models import UserType


class UserTest(TestCase):
    def test_user_details(self):
        self.assertTrue(self.artist.user.is_active)

        self.assertTrue(self.artist.user.is_artist)
        self.assertFalse(self.artist.user.is_customer)

    def test_artist_details(self):
        self.assertEqual(self.artist.user_name, "Van Gogh")
        self.assertEqual(self.artist.first_name, "Vincint")
        self.assertEqual(self.artist.last_name, "Gogh")
        self.assertEqual(self.artist.photo, self.picture)

    def test_admin_details(self):
        self.assertTrue(self.admin.is_staff)
        self.assertTrue(self.admin.is_superuser)
        self.assertEqual(self.admin.type, UserType.ADMIN)
