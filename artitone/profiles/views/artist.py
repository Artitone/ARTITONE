import logging

from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import CreateView

from artworks.models import Artwork
from profiles.forms.artist import ArtistChangeForm
from profiles.forms.artist import ArtistCreationForm
from profiles.models.artist import Artist
from profiles.models.user import User
from profiles.views.activate_email import activateEmail

logger = logging.getLogger("artitone")


class ArtistSignUpView(CreateView):
    """Displays a form for Artists to sign up with."""

    model = User
    form_class = ArtistCreationForm
    template_name = "registration/signup_form.html"

    def get_context_data(self, **kwargs):
        """Returns additional contextual information for display."""
        kwargs["user_type"] = "Artist"
        return super().get_context_data(**kwargs)

    @transaction.atomic
    def form_valid(self, form):
        """Saves the new user and logs them in."""
        user = form.save()
        user.is_active = True
        user.save()
        # try:
        #     activateEmail(self.request, user, form.cleaned_data.get("email"))
        # except Exception:
        #     user.delete()

        #     return redirect("signup")

        return redirect("login")


def view_artist_profile(request, pk):
    user = request.user
    if user.is_artist:
        artist = Artist.objects.get(user=pk)
        artist_change_form = ArtistChangeForm(None, instance=artist, prefix="artist")
        artwork_list = Artwork.objects.filter(artist=artist)
        logger.error(request.POST)
        if request.method == "GET":
            sort_method = request.GET.get("sort")
            if sort_method:
                if sort_method == "newest":
                    artwork_list = artwork_list.order_by("-pubdate")
                elif sort_method == "price_ltoh":
                    artwork_list = artwork_list.order_by("price")
                elif sort_method == "price_htol":
                    artwork_list = artwork_list.order_by("-price")
        elif request.method == "POST":
            form_type = request.POST["type"]
            if form_type == "artist_change":
                artist_change_form = ArtistChangeForm(
                    request.POST, request.FILES, instance=artist, prefix="artist"
                )
                if artist_change_form.is_valid():
                    artist_change_form.save()

        paginator = Paginator(artwork_list, 12)  # Show 25 contacts per page.

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            "profiles/artist_profile_page.html",
            {
                "artist": artist,
                "page_obj": page_obj,
                "artist_change_form": artist_change_form,
            },
        )
    else:
        return redirect("home")
