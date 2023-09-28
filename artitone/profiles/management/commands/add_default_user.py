"""The add_default_user command injects admin user into the database."""

from django.core.management.base import BaseCommand

# JSON model type representations.
from profiles.models.user import User



class Command(BaseCommand):
    help = "Loads missing categories."

    def handle(self, *args, **options):
        User.objects.create_superuser(email="admin@admin.com", password="admin")

