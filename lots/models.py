from django.db import models


class Lot(models.Model):
    starting = models.IntegerField(null=False, blank=False)
    increment = models.IntegerField(null=False, blank=False)
