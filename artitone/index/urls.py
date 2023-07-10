from django.urls import path

from index.views.home import home

urlpatterns = [
    path("", home, name="home"),
]
