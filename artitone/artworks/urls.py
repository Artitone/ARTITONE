from django.urls import path

from artworks.views import upload_artwork_image
from artworks.views import update_tags
from artworks.views import delete_artwork

urlpatterns = [
    path("", upload_artwork_image, name="upload_artwork"),
    path("<int:pk>", update_tags, name="update_tags"),
    path("<int:pk>/delete/", delete_artwork, name="delete_artwork"),
]
