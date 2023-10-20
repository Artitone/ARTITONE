import logging

from django.contrib.auth import login
from django.shortcuts import redirect
from django.shortcuts import render

from profiles.forms.artist import ArtistCreationForm
from profiles.forms.artist import UserLoginForm
from profiles.forms.customer import CustomerCreationForm
from profiles.views.activate_email import activateEmail

logger = logging.getLogger(__name__)


def about(request):
    """Directs the user to their home page."""
    login_form = UserLoginForm(None, prefix="login")
    artist_signup_form = ArtistCreationForm(None, prefix="artist")
    customer_signup_form = CustomerCreationForm(None, prefix="customer")

    if request.method == "POST":
        form_type = request.POST["type"]
        if form_type == "login":
            login_form = UserLoginForm(request.POST, prefix="login")
            if login_form.is_valid():
                user = login_form.login(request)
                if user:
                    login(request, user)
                    if user.is_artist:
                        return redirect("artist_profile_page", pk=request.user.pk)
                    elif user.is_customer:
                        return redirect("home")
                    else:
                        return redirect("home")
        elif form_type == "artist":
            artist_signup_form = ArtistCreationForm(request.POST, request.FILES, prefix="artist")
            if artist_signup_form.is_valid():
                user = artist_signup_form.save()
                user.is_active = False
                user.save()
                try:
                    activateEmail(request, user, user.email)
                except Exception:
                    user.delete()

                return redirect("home")
        elif form_type == "customer":
            customer_signup_form = CustomerCreationForm(
                request.POST, request.FILES, prefix="customer"
            )
            if customer_signup_form.is_valid():
                user = customer_signup_form.save()
                user.is_active = False
                user.save()
                try:
                    activateEmail(request, user, user.email)
                except Exception:
                    user.delete()

                return redirect("home")

    return render(
        request,
        "about.html",
        {
            "login_form": login_form,
            "artist_signup_form": artist_signup_form,
            "customer_signup_form": customer_signup_form,
        },
    )
