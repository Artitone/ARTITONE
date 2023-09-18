from django.urls import path

from artworks.views import upload_artwork
from artworks.views import delete_artwork
from artworks.views import purchase_artwork
from artworks.views import purchase_success
from artworks.views import purchase_fail

urlpatterns = [
    path("", upload_artwork, name="upload_artwork"),
    path("<int:pk>/delete/", delete_artwork, name="delete_artwork"),
    path("<int:pk>/purchase/", purchase_artwork, name="purchase_artwork"),
    path("<int:pk>/purchase/success", purchase_success, name="purchase_success"),
    path("<int:pk>/purchase/fail", purchase_fail, name="purchase_fail"),
]
