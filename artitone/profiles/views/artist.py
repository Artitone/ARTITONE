from django.db import transaction
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import CreateView

from profiles.forms.artist import ArtistCreationForm
from profiles.models import User
from profiles.models import Artist
from profiles.views.activate_email import activateEmail

from artworks.models import Artwork


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


def view_my_artworks(request, pk):
    user = request.user
    if user.is_artist:
        artist = Artist.objects.get(user=pk)
        artworks = Artwork.objects.filter(artist=artist)
        return render(
                request,
                "profiles/my_artworks.html",
                {"artworks": artworks},
            )
    else:
        return redirect("home")