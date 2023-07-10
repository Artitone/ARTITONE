from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import CreateView

from profiles.forms.customer import CustomerCreationForm
from profiles.models import User
from profiles.views.activate_email import activateEmail


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
