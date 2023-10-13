import logging
import time

from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from artworks.forms import CustomPayPalPaymentsForm
from artworks.models import Artwork

# from paypal.standard.forms import PayPalPaymentsForm
from profiles.models.artist import ArtistPaymentMethod
from profiles.models.customer import Customer
from purchases.models.order import Order
from purchases.models.purchase import Purchase

# Create your views here.


def purchase_artwork(request, pk):
    user = request.user
    if not user.is_customer:
        return redirect("home")

    artwork = Artwork.objects.get(pk=pk)
    artist = artwork.artist
    customer = Customer.objects.get(pk=user)
    order = Order.objects.create(
        customer=customer,
    )
    purchase = Purchase.objects.create(
        order=order,
        artwork=artwork,
        price=artwork.price,
    )

    payment_method = ArtistPaymentMethod.objects.get(pk=artist)

    # What you want the button to do.
    paypal_dict = {
        "business": payment_method.business_email,
        "amount": artwork.price,
        "item_name": artwork.title,
        "invoice": order.id,
        "notify_url": request.build_absolute_uri(reverse("paypal-ipn")),
        "return": request.build_absolute_uri(
            reverse("purchase_success", kwargs={"order_id": order.id})
        ),
        "cancel_return": request.build_absolute_uri(
            reverse("purchase_fail", kwargs={"order_id": order.id})
        ),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = CustomPayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)


def purchase_success(request, order_id):
    messages.success(request, f"Payment successfully made for {order_id}.")
    return redirect("home")


def purchase_fail(request, order_id):
    messages.error(request, f"Payment failed made for {order_id}!")
    return redirect("home")
