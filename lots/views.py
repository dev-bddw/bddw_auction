from django.shortcuts import get_object_or_404, render

from bids.forms import BidForm
from bids.models import Bid

from .models import Lot


# Create your views here.
def lot_detail_view(request, pk: int):
    form = BidForm
    lot = get_object_or_404(Lot, pk=pk)
    high_bid = Bid.objects.filter(lot=lot).order_by("-value")

    return render(
        request,
        "lot-detail-view.html",
        {"lot": lot, "high_bid": high_bid[0], "form": form},
    )


def bid_hx(request, pk: int):

    lot = get_object_or_404(Lot, pk=pk)

    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            form.user = request.user
            form.lot = lot
            form.save()

    return render(request, "partials/lot-poll-hx.html", {"lot": lot, "form": form})


def lot_poll_hx(request, pk: int):
    form = BidForm
    lot = get_object_or_404(Lot, pk=pk)
    high_bid = Bid.objects.filter(lot=lot).order_by("-value")

    return render(
        request,
        "partials/lot-poll-hx.html",
        {"lot": lot, "high_bid": high_bid[0], "form": form},
    )
