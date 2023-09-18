import logging

from django.contrib.auth import login
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from index.views.search import parse_search_filter
from profiles.forms.artist import ArtistCreationForm, UserLoginForm
from profiles.forms.customer import CustomerCreationForm
from profiles.views.activate_email import activateEmail

logger = logging.getLogger("artitone")


def home(request):
    """Directs the user to their home page."""
    # if request.user.is_authenticated:
    #     return redirect(f"profile/{request.user.pk}")
    login_form = UserLoginForm(None, prefix="login")
    artist_signup_form = ArtistCreationForm(None, prefix="artist")
    customer_signup_form = CustomerCreationForm(None, prefix="customer")
    logger.debug(
        f"============================\n {request.GET}\n\n {request.POST}\n================================="
    )
    filter = parse_search_filter(request.GET)
    artwork_list = filter.search()
    paginator = Paginator(artwork_list, 12)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        form_type = request.POST["type"]
        if form_type == "login":
            login_form = UserLoginForm(request.POST, prefix="login")
            if login_form.is_valid():
                user = login_form.login(request)
                if user:
                    login(request, user)
                    return redirect("home")
        elif form_type == "artist":
            artist_signup_form = ArtistCreationForm(
                request.POST, request.FILES, prefix="artist"
            )
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
                return redirect("home")

    return render(
        request,
        "index/index.html",
        {
            "page_obj": page_obj,
            "login_form": login_form,
            "artist_signup_form": artist_signup_form,
            "customer_signup_form": customer_signup_form,
        },
    )
