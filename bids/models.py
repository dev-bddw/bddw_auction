from django.db import models


class Bid(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    value = models.IntegerField(null=False, blank=False)
    lot = models.ForeignKey("lots.Lot", on_delete=models.CASCADE)
