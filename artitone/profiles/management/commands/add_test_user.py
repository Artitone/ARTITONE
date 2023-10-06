"""The add_default_user command injects admin user into the database."""

from django.core.management.base import BaseCommand

from profiles.models.artist import Artist
from profiles.models.customer import Customer

# JSON model type representations.
from profiles.models.user import User
from profiles.models.user import UserType


class Command(BaseCommand):
    help = "Create test accounts"

    def handle(self, *args, **options):
        del args  # Unused.
        artist_email = "dif-axayasu61829476@hotmail.com"
        customer_email = "tamra_montoya32182948@outlook.com"
        password = "test1_Test2_test3"

        if not User.objects.filter(email=artist_email).exists():
            Artist.objects.create(
                user=User.objects.create_user(
                    email=artist_email,
                    password=password,
                    is_active=True,
                    type=UserType.ARTIST,
                ),
                user_name="test_artist",
            )
            self.stdout.write(self.style.SUCCESS("Successfully created test artist."))
        else:
            self.stdout.write(self.style.SUCCESS("Test artist with email address already exists."))
        if not User.objects.filter(email=customer_email).exists():
            Customer.objects.create(
                user=User.objects.create_user(
                    email=customer_email,
                    password=password,
                    is_active=True,
                    type=UserType.CUSTOMER,
                ),
                user_name="test_customer",
            )
            self.stdout.write(self.style.SUCCESS("Successfully created test customer."))
        else:
            self.stdout.write(
                self.style.SUCCESS("Test customer with email address already exists.")
            )
