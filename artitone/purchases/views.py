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

logger = logging.getLogger(__name__)
# Create your views here.


def purchase_artwork(request, pk):
    user = request.user
    if not user.is_customer:
        return redirect("home")

    artwork = Artwork.objects.get(pk=pk)

    if artwork.status != Artwork.PUBLISHED:
        messages.error(
            request,
            (
                f"Sorry, the artwork {artwork} you've just browsed is currently unavailable.\n"
                "Please understand that the artwork may have been acquired by another buyer,"
                "we kindly suggest you check again later."
            ),
        )
        return redirect("home")
    artist = artwork.artist
    customer = Customer.objects.get(pk=user)

    if (
        Purchase.objects.filter(artwork=artwork)
        and Purchase.objects.get(artwork=artwork).order.customer == customer
    ):
        purchase = Purchase.objects.get(artwork=artwork)
        order = purchase.order
    elif not Purchase.objects.filter(artwork=artwork):
        order = Order.objects.create(
            customer=customer,
        )
        purchase = Purchase.objects.create(
            order=order,
            artwork=artwork,
            price=artwork.price,
        )
    else:
        messages.error(
            request,
            (
                f"Sorry, the artwork {artwork} you've just browsed is currently unavailable.\n"
                "Please understand that the artwork may have been acquired by another buyer,"
                "we kindly suggest you check again later."
            ),
        )
        return redirect("home")

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
    update_artwork_status(order_id)
    return redirect("home")


def purchase_fail(request, order_id):
    messages.error(request, f"Payment failed made for {order_id}!")
    order = Order.objects.get(pk=order_id)
    logger.debug(f"{order} successfully deleted!")
    order.delete()
    return redirect("home")


def update_artwork_status(order_id):
    order = Order.objects.get(pk=order_id)
    for purchase in order.purchases.all():
        purchase.artwork.status = Artwork.IN_PROGRESS
        purchase.artwork.save()
        logger.debug(f"Update {purchase.artwork} status to {Artwork.IN_PROGRESS}")
