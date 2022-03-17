from django.urls import path

from .views import cart_view

app_name = "account"

urlpatterns = [path("my-cart/", view=cart_view, name="cart")]
