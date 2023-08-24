"""The load_categories command injects missing categories into the database."""

import json

from django.core.management.base import BaseCommand

# JSON model type representations.
from artworks.models import Category


class Command(BaseCommand):
    help = "Loads missing categories."

    def add_arguments(self, parser):
        parser.add_argument(
            "--category_data",
            default="artworks/fixtures/category.json",
            help="The path to the data (in JSON format).",
        )

    def handle(self, *args, **options):
        del args  # Unused.
        with open(options["category_data"]) as raw_data:
            data = json.loads(raw_data.read())

        for entry in data:
            name = entry["fields"]["name"]
            if Category.objects.filter(name=name).exists():
                continue

            Category.objects.create(**entry["fields"])
            self.stdout.write(self.style.SUCCESS(f"Successfully created {repr(name)}."))
