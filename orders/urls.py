from django.urls import path

from .views import (
    cart_view,
    stripe_config,
    create_checkout_session,
)

app_name = "account"

urlpatterns = [
    path("my-cart/", view=cart_view, name="cart"),
    path("my-public-key/", view=stripe_config, name="public-key"),
    path("create-checkout-session/", view=create_checkout_session, name="create_session")
]
