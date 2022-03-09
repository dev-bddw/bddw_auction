from django.db import models
from django.utils import timezone

from bids.models import Bid


class Lot(models.Model):
    starting = models.IntegerField(null=False, blank=False)
    increment = models.IntegerField(null=False, blank=False)

    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=False, blank=False)

    def current_high_bid(self):
        if Bid.objects.filter(lot=self):
            return Bid.objects.filter(lot=self).order_by("-value")[0].value
        else:
            Lot.objects.get(pk=self.pk)
            return self.starting

    def current_high_bidder(self):
        if Bid.objects.filter(lot=self):
            return Bid.objects.filter(lot=self).order_by("-value")[0].user
        else:
            return "No High Bidder"

    def is_over(self):
        return timezone.now() > self.end_time

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("lots:lot-detail", kwargs={"pk": self.pk})
