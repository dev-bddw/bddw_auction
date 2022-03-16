from django.urls import path

from .views import (
    bid_hx,
    lazy_cron_endpoint,
    lot_detail_poll_hx,
    lot_detail_view,
    lot_list_poll_hx,
    lot_list_view,
    lot_upload,
)

app_name = "lots"

urlpatterns = [
    path("<pk>", view=lot_list_view, name="lot-list"),
    path("auction-end/", view=lazy_cron_endpoint, name="endpoint"),
    path("lot-upload/", view=lot_upload, name="lot-upload"),
    path("lot/<pk>/", view=lot_detail_view, name="lot-detail"),
    # htmx
    path("bid/<pk>", view=bid_hx, name="bid"),
    path("detail-hxpoll/<pk>", view=lot_detail_poll_hx, name="detail-poll"),
    path("list-hxpoll/<pk>", view=lot_list_poll_hx, name="list-poll"),
]
