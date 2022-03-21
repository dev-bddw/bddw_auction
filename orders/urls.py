from django.urls import path

from .views import (
    cart_view,
    checkout_failure,
    checkout_success,
    create_checkout_session,
    stripe_config,
)

app_name = "account"

urlpatterns = [
    path("my-cart/", view=cart_view, name="cart"),
    path("my-public-key/", view=stripe_config, name="public-key"),
    path(
        "create-checkout-session/", view=create_checkout_session, name="create_session"
    ),
    path("success/", view=checkout_success),
    path("cancelled/", view=checkout_failure),
]
