"""The add_default_user command injects admin user into the database."""

from django.core.management.base import BaseCommand

# JSON model type representations.
from profiles.models.user import User
from profiles.models.user import UserType


class Command(BaseCommand):
    help = "Add superuser"

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            default="admin@admin.com",
            help="The email address of the super user to create.",
        )
        parser.add_argument(
            "--password",
            default="admin",
            help="The password of the super user to create.",
        )

    def handle(self, *args, **options):
        del args  # Unused.
        email = options["email"]

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                password=options["password"],
                is_active=True,
                type=UserType.ADMIN,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created super user for {repr(email)}.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Super user with email address {repr(email)} already exists.")
            )
