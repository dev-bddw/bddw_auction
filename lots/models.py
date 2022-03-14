from django.db import models
from django.utils import timezone

from bids.models import Bid

# the acutal bid doesn't matter much.
# what matters is that we know who has the highest bid
# and what the next highest OTHER person bid that determines the actual current bid
# this is how proxy bidding works


class Auction(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)
    description = models.TextField(blank=True, null=True, max_length=300)


class Lot(models.Model):
    starting = models.IntegerField(null=False, blank=False)
    increment = models.IntegerField(null=False, blank=False)

    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=False, blank=False)

    auction = models.ForeignKey(
        "Auction", blank=True, null=True, on_delete=models.CASCADE
    )

    def has_bids(self):
        return len(Bid.objects.filter(lot=self)) > 0

    def current_high_bid(self):
        return self.return_next_high_bid_plus_increment()

    def actual_proxy_bid(self):
        return Bid.objects.filter(lot=self).order_by("-value")[0].value

    def current_high_bidder(self):
        if Bid.objects.filter(lot=self):
            return Bid.objects.filter(lot=self).order_by("-value")[0].user
        else:
            return "No High Bidder"

    def is_over(self):
        return timezone.now() > self.end_time

    def return_next_high_bid_plus_increment(self):
        try:
            return (
                Bid.objects.filter(lot=self)
                .exclude(user=self.current_high_bidder())
                .order_by("-value")[0]
                .value
                + self.increment
            )
        except (IndexError, ValueError):
            return self.increment * 2

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("lots:lot-detail", kwargs={"pk": self.pk})

    def winner(self):
        if self.is_over():
            return self.current_high_bidder()
        else:
            return "Auction not over yet"
