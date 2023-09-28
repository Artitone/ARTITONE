from django.contrib import admin

from artworks.models import Artwork
from artworks.models import IndustrialModel

# Register your models here.

admin.site.register(Artwork)
admin.site.register(IndustrialModel)
