from django.urls import path

from .views import (
    cart_view,
    checkout_failure,
    checkout_success,
    create_checkout_session,
    orders_detail_view,
    orders_list_view,
    stripe_config,
    stripe_webhook,
)

app_name = "account"

urlpatterns = [
    path("my-cart/", view=cart_view, name="cart"),
    path("my-public-key/", view=stripe_config, name="public-key"),
    path(
        "create-checkout-session/", view=create_checkout_session, name="create_session"
    ),
    path("my-orders/", view=orders_list_view, name="orders"),
    path("my-orders/<pk>", view=orders_detail_view, name="orders-detail"),
    path("success/", view=checkout_success),
    path("cancelled/", view=checkout_failure),
    path("webhook", view=stripe_webhook),
]
