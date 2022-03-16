from django.forms import HiddenInput, ModelForm, NumberInput

from .models import Bid


class BidForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # https://stackoverflow.com/questions/1697702/how-to-pass-initial-parameter-to-djangos-modelform-instance
        try:
            step = kwargs.pop("step")
        except KeyError:
            step = 0
        super(BidForm, self).__init__(*args, **kwargs)
        self.fields["value"].label = ""
        self.fields["value"].widget.attrs.update(step=step)

    class Meta:
        model = Bid
        fields = ["value", "user", "lot"]
        widgets = {"value": NumberInput(), "user": HiddenInput(), "lot": HiddenInput()}
