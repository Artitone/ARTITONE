from django.urls import path

from index.views.home import home
from index.views.about import about

urlpatterns = [
    path("", home, name="home"),
    path("/about", about, name="about"),
]
