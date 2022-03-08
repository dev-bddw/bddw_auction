from django.urls import path

from .views import bid_hx, lot_detail_view, lot_list_view, lot_poll_hx

app_name = "lots"

urlpatterns = [
    path("", view=lot_list_view, name="lot-list"),
    path("<pk>/", view=lot_detail_view, name="lot-detail"),
    # htmx
    path("bid/<pk>", view=bid_hx, name="bid"),
    path("poll/<pk>", view=lot_poll_hx, name="poll"),
]
