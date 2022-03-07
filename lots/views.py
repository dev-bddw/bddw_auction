from django.shortcuts import get_object_or_404, render

from bids.forms import BidForm
from bids.models import Bid

from .models import Lot


def return_high_bid(lot):
    if Bid.objects.filter(lot=lot):
        return Bid.objects.filter(lot=lot).order_by("-value")[0]
    else:
        return lot.starting


def lot_detail_view(request, pk: int):
    user = request.user
    lot = get_object_or_404(Lot, pk=pk)

    form = BidForm(
        {
            "inc_step": lot.increment,
            "value": return_high_bid(lot),
            "user": user,
            "lot": lot,
        }
    )

    return render(
        request,
        "lot-detail-view.html",
        {"lot": lot, "high_bid": return_high_bid(lot), "form": form},
    )


def bid_hx(request, pk: int):

    lot = get_object_or_404(Lot, pk=pk)

    if request.method == "POST":
        bid = request.POST["value"]
        form = BidForm(request.POST)

        if form.is_valid() and int(request.POST["value"]) > return_high_bid(lot):
            form = form.save()
            message = f"Your of {bid} bid was placed successfully"

        elif not form.is_valid():
            message = f"There was a problem with your form value, your bid of {bid} was unsuccessful"

        else:
            message = f"Your bid of {bid} was not higher than the current high bid."

        return render(request, "partials/bid-modal-hx.html", {"message": message})


def lot_poll_hx(request, pk: int):
    form = BidForm
    lot = get_object_or_404(Lot, pk=pk)

    return render(
        request,
        "partials/lot-poll-hx.html",
        {"lot": lot, "high_bid": return_high_bid(lot), "form": form},
    )
