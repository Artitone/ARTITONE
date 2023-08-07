from django.urls import path

from profiles.views.activate_email import activate
from profiles.views.profile import ProfileView
from profiles.views.profile import SignUpView
from profiles.views.artist import ArtistSignUpView
from profiles.views.artist import view_my_artworks
from profiles.views.customer import CustomerSignUpView


urlpatterns = [
    path("<int:pk>", ProfileView.as_view(), name="profile"),
    path("activate/<uidb64>/<token>", activate, name="activate"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path(
        "accounts/signup/artist/",
        ArtistSignUpView.as_view(),
        name="artist_signup",
    ),
    path(
        "accounts/signup/customer/",
        CustomerSignUpView.as_view(),
        name="customer_signup",
    ),
    path("<int:pk>/my_artworks", view_my_artworks, name="my_artworks"),
]