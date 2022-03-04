from django.forms import ModelForm, NumberInput

from .models import Bid


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["value"]
        widets = {"value": NumberInput()}
