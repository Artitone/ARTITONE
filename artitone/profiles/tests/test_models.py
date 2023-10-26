from profiles.models.artist import Artist
from profiles.models.following import UserFollowing
from profiles.models.following import follow
from profiles.models.following import unfollow
from profiles.models.user import UserType
from profiles.tests.unittest_setup import TestCase


class UserTest(TestCase):
    def test_user_details(self):
        self.assertTrue(self.artist.user.is_active)

        self.assertTrue(self.artist.user.is_artist)
        self.assertFalse(self.artist.user.is_customer)

    def test_artist_details(self):
        self.assertEqual(self.artist.user_name, "Van Gogh")
        self.assertEqual(self.artist.first_name, "Vincint")
        self.assertEqual(self.artist.last_name, "Gogh")
        self.assertEqual(self.artist.photo, self.picture.picture)

    def test_admin_details(self):
        self.assertTrue(self.admin.is_staff)
        self.assertTrue(self.admin.is_superuser)
        self.assertEqual(self.admin.type, UserType.ADMIN)


class TestUserFollowing(TestCase):
    def setUp(self):
        super().setUp()

    def test_follow(self):
        self.assertEqual(self.customer.following.all().count(), 0)
        self.assertEqual(self.artist.followers.all().count(), 0)
        follow(self.customer, self.artist)
        self.assertEqual(self.customer.following.all().count(), 1)
        self.assertEqual(self.artist.followers.all().count(), 1)

    def test_unfollow(self):
        self.assertEqual(self.customer.following.all().count(), 0)
        self.assertEqual(self.artist.followers.all().count(), 0)
        follow(self.customer, self.artist)
        self.assertEqual(self.customer.following.all().count(), 1)
        self.assertEqual(self.artist.followers.all().count(), 1)
        unfollow(self.customer, self.artist)
        self.assertEqual(self.customer.following.all().count(), 0)
        self.assertEqual(self.artist.followers.all().count(), 0)
