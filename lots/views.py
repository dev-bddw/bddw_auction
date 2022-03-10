from django.shortcuts import get_object_or_404, render

from bids.forms import BidForm

from .models import Lot


def lot_list_view(request):

    return render(request, "lot-list-view.html", {"lots": Lot.objects.all()})


def lot_detail_view(request, pk: int):
    user = request.user
    lot = get_object_or_404(Lot, pk=pk)

    form = BidForm(
        {
            "value": lot.current_high_bid() + 100,
            "user": user,
            "lot": lot,
        }
    )

    return render(
        request,
        "lot-detail-view.html",
        {"lot": lot, "form": form},
    )


def bid_hx(request, pk: int):

    lot = get_object_or_404(Lot, pk=pk)

    if request.method == "POST":
        bid = request.POST["value"]
        form = BidForm(request.POST)

        if form.is_valid() and int(request.POST["value"]) > lot.current_high_bid():

            if request.user == lot.current_high_bidder():
                if lot.actual_proxy_bid() > int(request.POST["value"]):
                    message = f"Your bid of {bid} was not more than your proxy bid"
                else:
                    form = form.save()
                    message = f"Your bid of {bid} bid was placed successfully"
            else:
                form = form.save()
                message = f"Your of {bid} bid was placed successfully"

        elif not form.is_valid():
            message = f"There was a problem with your form value, your bid of {bid} was unsuccessful"

        else:
            message = f"Your bid of {bid} was not higher than the current high bid."

        return render(request, "partials/bid-modal-hx.html", {"message": message})


def lot_detail_poll_hx(request, pk: int):
    user = request.user
    lot = get_object_or_404(Lot, pk=pk)
    form = BidForm(
        {
            "value": lot.current_high_bid() + 100,
            "user": user,
            "lot": lot,
        }
    )
    lot = get_object_or_404(Lot, pk=pk)

    return render(
        request,
        "partials/lot-detail-poll-hx.html",
        {"lot": lot, "form": form},
    )


def lot_list_poll_hx(request, pk: int):
    lot = get_object_or_404(Lot, pk=pk)

    return render(request, "partials/lot-list-poll-hx.html", {"lot": lot})


# https://htmx-django.com/blog/how-to-implement-countdown-timer-in-django-via-htm
# def time_difference(request):
#     #go live date is 12/01/2021
#     delta = datetime(2021, 12, 1, tzinfo=timezone.utc) - timezone.now()

#     return render(
#         request,
#         "components/time_difference.html",
#         {
#             "days": delta.days,
#             "seconds": delta.seconds % 60,
#             "minutes": (delta.seconds // 60) % 60,
#             "hours": delta.seconds // 3600,
#         },
#     )
