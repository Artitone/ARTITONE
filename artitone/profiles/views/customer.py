from functools import wraps
import logging

from django.db import transaction
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import CreateView

from artworks.models import Artwork
from profiles.forms.customer import CustomerCreationForm
from profiles.models.artist import Artist
from profiles.models.customer import Customer
from profiles.models.following import UserFollowing
from profiles.models.following import follow
from profiles.models.following import unfollow
from profiles.models.user import User
from profiles.views.activate_email import activateEmail

logger = logging.getLogger(__name__)


def customers_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_anonymous or not user.is_customer:
            return redirect("home")
        else:
            return function(request, *args, **kwargs)

    return wrap


class CustomerSignUpView(CreateView):
    """Displays a form for volunteers to sign up with."""

    model = User
    form_class = CustomerCreationForm
    template_name = "registration/signup_form.html"
    # volunteer_profile = {}

    def get_context_data(self, **kwargs):
        """Returns additional contextual information for display."""
        kwargs["user_type"] = "Customer"
        return super().get_context_data(**kwargs)

    @transaction.atomic
    def form_valid(self, form):
        """Saves the new user and logs them in."""
        user = form.save()
        user.is_active = True
        user.save()
        try:
            activateEmail(self.request, user, form.cleaned_data.get("email"))
        except Exception:
            user.delete()

            return redirect("signup")

        return redirect("login")


@customers_only
def view_basket(request, pk):
    customer = Customer.objects.get(pk=request.user)
    page_obj = customer.basket.all()

    return render(
        request,
        "profiles/customer_basket.html",
        {
            "page_obj": page_obj,
        },
    )


@customers_only
def add_to_basket(request, artwork_pk):
    customer = Customer.objects.get(pk=request.user)
    artwork = Artwork.objects.get(pk=artwork_pk)
    customer.basket.add(artwork)
    return redirect("basket", pk=customer.pk)


@customers_only
def follow_artist(request, artist_pk):
    customer = Customer.objects.get(pk=request.user)
    artist = Artist.objects.get(pk=artist_pk)

    if customer.following.filter(following_user_id=artist):
        unfollow(customer, artist)
        logger.debug(f"{customer} unfollows {artist}")
    else:
        following = follow(customer, artist)
        logger.debug(f"customer follows artist: {following}")
    return redirect("artist_profile_page", pk=artist_pk)
