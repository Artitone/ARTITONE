from venv import logger

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode

from artitone.settings import AWS_SES_DOMAIN
from artitone.settings import DEFAULT_FROM_EMAIL


class ActivationError(Exception):
    pass


def activateEmail(request, user, to_email):
    """Creates activation link and sends email to user"""

    subject = "Account Activation"
    message = render_to_string(
        "registration/template_activate_account.html",
        {
            "email": user.email,
            "user": user,
            "domain": AWS_SES_DOMAIN if AWS_SES_DOMAIN else "127.0.0.1:8000",
            "site_name": "ArtitoneUS",
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    try:
        send_mail(
            subject,
            message,
            DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False,
        )
        messages.success(
            request,
            (
                f"Dear {user}, please go to your email inbox and click on "
                "the received activation link to confirm and complete the registration. "
                "Note: Check your spam folder."
            ),
        )
    except BadHeaderError:
        return HttpResponse("Invalid header found.")
    except Exception as e:
        messages.error(
            request,
            (
                "It seems we encountered an error while sending the activation email."
                "Please try again soon."
            ),
        )
        logger.exception(e)
        raise ActivationError()


def activate(request, uidb64, token):
    """Activates user once activation link is used"""
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and token:
        user.is_active = True
        user.save()
        messages.success(
            request,
            "Thank you for your email confirmation. Now you can login your account.",
        )
        return redirect("login")
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect("signup")
