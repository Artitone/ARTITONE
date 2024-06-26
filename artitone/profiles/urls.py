from django.urls import path

from profiles.views.activate_email import activate
from profiles.views.artist import ArtistSignUpView
from profiles.views.artist import view_artist_profile
from profiles.views.customer import CustomerSignUpView
from profiles.views.customer import add_to_basket
from profiles.views.customer import follow_artist
from profiles.views.customer import view_basket
from profiles.views.profile import ProfileView
from profiles.views.profile import SignUpView

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
    path("<int:pk>/artist_profile_page", view_artist_profile, name="artist_profile_page"),
    path("<int:pk>/basket", view_basket, name="basket"),
    path("add_to_basket/<int:artwork_pk>/", add_to_basket, name="add_to_basket"),
    path("follow_artist/<int:artist_pk>/", follow_artist, name="follow_artist"),
]
