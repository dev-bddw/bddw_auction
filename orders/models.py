from django.db import models

from bddw_auction.users.models import User
from lots.models import Lot


class Cart(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.PROTECT)
    total_value = models.DecimalField(
        default=0, blank=True, null=True, max_digits=10, decimal_places=2
    )

    def save(self, *args, **kwargs):
        self.total_value = self.get_cart_value()
        super(Cart, self).save(*args, **kwargs)

    def get_cart_value(self):
        prices = [x.price for x in self.lots()]
        return sum(prices)

    def lots(self):
        return Lot.objects.filter(cart=self)

    def update_cart_value(self):
        self.save()


class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    paid = models.BooleanField(default=False, blank=False, null=False)
    items_value = models.DecimalField(
        default=0, blank=True, null=True, max_digits=10, decimal_places=2
    )
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

    # stripe

    stripe_checkout_session_id = models.CharField(
        default=None, blank=True, null=True, max_length=200
    )
    stripe_session_data = models.CharField(blank=True, null=True, max_length=10000)
