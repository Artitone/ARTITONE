"""The add_default_user command injects admin user into the database."""

from django.core.management.base import BaseCommand

# JSON model type representations.
from profiles.models.user import User


class Command(BaseCommand):
    help = "Loads missing categories."

    def handle(self, *args, **options):
        if not User.objects.filter(email="admin@admin.com").exists():
            User.objects.create_superuser(email="admin@admin.com", password="admin")
