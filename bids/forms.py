from django.forms import HiddenInput, ModelForm, NumberInput

from .models import Bid


class BidForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)

        self.fields["value"].label = ""
        self.fields["value"].widget.attrs.update(step=100)

    class Meta:
        model = Bid
        fields = ["value", "user", "lot"]
        widgets = {"value": NumberInput(), "user": HiddenInput(), "lot": HiddenInput()}
