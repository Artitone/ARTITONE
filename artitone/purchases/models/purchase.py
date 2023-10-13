from django.db import models

from artworks.models import Artwork
from purchases.models.order import Order

# Create your models here.


class Purchase(models.Model):
    order = models.ForeignKey(Order, related_name="purchases", on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    price = models.FloatField(default=0)

    class Meta:
        unique_together = ("order", "artwork")
