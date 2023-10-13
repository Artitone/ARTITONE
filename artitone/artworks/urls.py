from django.urls import path

from artworks.views import delete_artwork
from artworks.views import upload_artwork

urlpatterns = [
    path("", upload_artwork, name="upload_artwork"),
    path("<int:pk>/delete/", delete_artwork, name="delete_artwork"),
]
