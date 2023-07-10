from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import CreateView

from profiles.forms.artist import ArtistCreationForm
from profiles.models import User
from profiles.views.activate_email import activateEmail


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
        try:
            activateEmail(self.request, user, form.cleaned_data.get("email"))
        except Exception:
            user.delete()

            return redirect("signup")

        return redirect("login")
