from django.urls import path

from purchases.views import purchase_artwork
from purchases.views import purchase_fail
from purchases.views import purchase_success

urlpatterns = [
    path("<int:pk>/purchase/", purchase_artwork, name="purchase_artwork"),
    path("<uuid:order_id>/purchase/success", purchase_success, name="purchase_success"),
    path("<uuid:order_id>/purchase/fail", purchase_fail, name="purchase_fail"),
]
