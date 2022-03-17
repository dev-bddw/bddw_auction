from django.db import models

from bddw_auction.users.models import User


class Cart(models.Model):
    order = models.ForeignKey("Order", blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    total_value = models.DecimalField(
        default=0, blank=True, null=True, max_digits=10, decimal_places=2
    )


class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    paid = models.BooleanField()
    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        blank=True,
        null=True,
    )
    shipping = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        blank=True,
        null=True,
    )
