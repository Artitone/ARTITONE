from django.urls import path

from index.views.about import about
from index.views.home import home
from index.views.shop_interface import shop_interface

urlpatterns = [
    path("", home, name="home"),
    path("/about", about, name="about"),
    path("/shop_interface", shop_interface, name="shop_interface"),
]
