import os

from django.db import models
from django.utils import timezone

from bddw_auction.users.models import User
from bids.models import Bid

# the acutal bid doesn't matter much.
# what matters is that we know who has the highest bid
# and what the next highest OTHER person bid that determines the actual current bid
# this is how proxy bidding works


class Auction(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)
    description = models.TextField(blank=True, null=True, max_length=300)
    is_active = models.BooleanField(default=False, blank=False, null=False)


class LotImage(models.Model):
    img = models.ImageField(default=None, null=True, upload_to="lots")
    file_name = models.CharField(default=None, null=True, max_length=100)

    def __str__(self):
        return self.file_name

    def save(self, *args, **kwargs):
        self.file_name = self.base_file()
        super(LotImage, self).save(*args, **kwargs)

    def base_file(self):
        # we need to overwrite save method and create a char-field for file name and
        # use this method to set the filename char field
        return os.path.basename(self.img.path)


class Lot(models.Model):
    sku = models.CharField(blank=True, null=True, max_length=300)
    name = models.CharField(blank=True, null=True, max_length=300)
    description = models.TextField(blank=True, null=True, max_length=500)

    img = models.ImageField(default=None, null=True, upload_to="lots")

    starting = models.IntegerField(null=False, blank=False)
    increment = models.IntegerField(null=False, blank=False)

    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=False, blank=False)

    auction = models.ForeignKey(
        "Auction", blank=True, null=True, on_delete=models.CASCADE
    )

    # end of auction behavior

    winner = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    price = models.IntegerField(default=0, null=True)
    is_closed = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    cart = models.ForeignKey(
        "orders.Cart", blank=True, null=True, on_delete=models.PROTECT
    )
    order = models.ForeignKey(
        "orders.Order", blank=True, null=True, on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name

    def has_bids(self):
        return len(Bid.objects.filter(lot=self)) > 0

    def current_high_bid(self):
        if not self.has_bids():
            return self.starting
        else:
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

    # call with cron job at end of auction
    def end_auction(self):
        if self.is_over() and self.has_bids() and not self.is_closed:
            self.winner = self.current_high_bidder()
            self.price = self.current_high_bid()
            self.is_closed = True
            self.save()
            return 1
        else:
            return 0
