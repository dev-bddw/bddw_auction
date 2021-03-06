import csv
import io

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from bids.forms import BidForm

from .cron import end_of_auction
from .models import Auction, Lot, LotImage


def lot_list_view(request, pk: int):
    return render(
        request,
        "lot-list-view.html",
        {
            "auction": Auction.objects.get(id=pk),
            "lots": Lot.objects.filter(auction_id=pk),
        },
    )


def lazy_cron_endpoint(request):
    status = end_of_auction()
    return HttpResponse(f"{status}")


def lot_detail_view(request, pk: int):
    user = request.user
    lot = get_object_or_404(Lot, pk=pk)

    images = LotImage.objects.filter(file_name__startswith=lot.sku)

    form = BidForm(
        {
            "value": lot.current_high_bid() + lot.increment,
            "user": user,
            "lot": lot,
        },
        step=lot.increment,
    )

    return render(
        request,
        "lot-detail-view.html",
        {"lot": lot, "form": form, "images": images},
    )


def lot_upload(request):

    if request.method == "POST":

        csv_file = request.FILES["file"]
        # let's check if it is a csv file
        if not csv_file.name.endswith(".csv"):
            pass
            # messages.error(request, 'THIS IS NOT A CSV FILE')
        data_set = csv_file.read().decode("UTF-8")
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=",", quotechar='"'):
            Lot.objects.update_or_create(
                sku=column[0],
                name=column[1],
                description=column[2],
                auction=Auction.objects.get(pk=column[3]),
                starting=column[4],
                increment=column[5],
                start_time=column[6],
                end_time=column[7],
                img=column[8],
            )
            if column[9]:
                LotImage.objects.update_or_create(img=column[9])
            if column[10]:
                LotImage.objects.update_or_create(img=column[10])
            if column[11]:
                LotImage.objects.update_or_create(img=column[11])
            if column[12]:
                LotImage.objects.update_or_create(img=column[12])
            if column[13]:
                LotImage.objects.update_or_create(img=column[13])
            if column[14]:
                LotImage.objects.update_or_create(img=column[14])
            if column[15]:
                LotImage.objects.update_or_create(img=column[15])
            if column[16]:
                LotImage.objects.update_or_create(img=column[16])

        return render(request, "lot-upload.html", {})

    else:
        return render(request, "lot-upload.html", {})


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
                    message = f"Your proxy bid was succesfully increased to {bid}."
            else:
                # you've been outbid email
                # outbid = lot.current_high_bidder()
                form = form.save()
                message = f"Your of {bid} bid was placed successfully."

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
            "value": lot.current_high_bid() + lot.increment,
            "user": user,
            "lot": lot,
        },
        step=lot.increment,
    )
    lot = get_object_or_404(Lot, pk=pk)

    return render(
        request,
        "partials/lot-detail-poll-hx.html",
        {"lot": lot, "form": form},
    )


def lot_list_poll_hx(request, pk: int):
    auction = get_object_or_404(Auction, pk=pk)
    lots = Lot.objects.filter(auction=auction)
    return render(
        request, "partials/lot-list-poll-hx.html", {"auction": auction, "lots": lots}
    )


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
