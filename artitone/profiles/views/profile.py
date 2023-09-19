from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError
from django.core.mail import send_mail
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import DetailView
from django.views.generic import TemplateView

from artitone.settings import AWS_SES_DOMAIN
from artitone.settings import DEFAULT_FROM_EMAIL
from profiles.forms.artist import ArtistChangeForm
from profiles.forms.customer import CustomerChangeForm
from profiles.models import Artist
from profiles.models import Customer
from profiles.models import User


class SignUpView(TemplateView):
    """Generic signup where users can select their user type."""

    template_name = "registration/signup.html"


@method_decorator([login_required], name="dispatch")
class ProfileView(DetailView):
    """Displays a user's profile and additional type specific information."""

    # id = User.pk
    model = User
    context_object_name = "user"
    template_name = "profiles/profile.html"
    pk_url_kwarg = "user_id"

    def get_object(self, *args, **kwargs):
        """Returns the user object for display."""
        pk = self.kwargs["pk"]
        return get_object_or_404(User, pk=pk)

    def get_context_data(self, **kwargs):
        """Returns additional contextual information for display."""
        pk = self.kwargs["pk"]
        user = get_object_or_404(User, pk=pk)
        kwargs["curr_user"] = self.request.user
        if user.is_artist:
            artist_profile = Artist.objects.get(pk=user)
            kwargs["artist"] = artist_profile
            kwargs["user_form"] = ArtistChangeForm(instance=artist_profile)

        if user.is_customer:
            customer_profile = Customer.objects.get(pk=user)
            kwargs["customer"] = customer_profile
            kwargs["user_form"] = CustomerChangeForm(instance=customer_profile)

        return super().get_context_data(**kwargs)

    def password_reset_request(request):
        if request.method == "POST":
            password_reset_form = PasswordResetForm(request.POST)
            if password_reset_form.is_valid():
                data = password_reset_form.cleaned_data["email"]
                associated_user = User.objects.filter(Q(email=data)).first()
                if associated_user:
                    subject = "Password Reset Request"
                    message = render_to_string(
                        "template_reset_password.html",
                        {
                            "email": associated_user.email,
                            "user": associated_user,
                            "domain": AWS_SES_DOMAIN if AWS_SES_DOMAIN else "127.0.0.1:8000",
                            "site_name": "ARTITONE",
                            "uid": urlsafe_base64_encode(force_bytes(associated_user.pk)),
                            "token": default_token_generator.make_token(associated_user),
                            "protocol": "https" if request.is_secure() else "http",
                        },
                    )
                    try:
                        send_mail(
                            subject,
                            message,
                            DEFAULT_FROM_EMAIL,
                            [associated_user.email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                    return redirect("/password_reset/done/")
        password_reset_form = PasswordResetForm()
        return render(
            request=request,
            template_name="password_reset.html",
            context={"password_reset_form": password_reset_form},
        )


def profile_update(request, userid):
    """Get profile update POST and call save function on ChangeForms."""

    userid = request.user.pk
    userid = userid
    profile = get_object_or_404(User, pk=request.user.pk)

    if request.user.is_customer:
        profile = get_object_or_404(Customer, pk=request.user)
        form = CustomerChangeForm(
            request.POST,
            request.FILES,
            instance=profile,
        )
    elif request.user.is_artist:
        profile = get_object_or_404(Artist, pk=request.user)
        form = ArtistChangeForm(request.POST, request.FILES, instance=profile)
    else:
        raise ValueError("profile_update: user must either a volunteer or an organizaiton.")
    form.save()
    return redirect("home")


# This part is for Customer specified features.


# This part is for Artist specified features.
