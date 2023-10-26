import uuid

from django.db import models

from profiles.models.customer import Customer

# Create your models here.


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        Customer, related_name="orders", on_delete=models.CASCADE, null=True
    )
    payment_success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    discount = models.FloatField(default=0, null=False, blank=False)

    def get_total_price(self):
        total_price = 0
        for purchase in self.purchases.all():
            total_price += purchase.price

        return total_price * (1 - self.discount)
