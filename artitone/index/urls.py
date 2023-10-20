from django.urls import path

from index.views.about import about
from index.views.home import home

urlpatterns = [
    path("", home, name="home"),
    path("/about", about, name="about"),
]
