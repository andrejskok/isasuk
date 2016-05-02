from django.utils.translation import ugettext as _
from django import forms

class MeetingForm(forms.Form):
    title =  forms.CharField(label=_("Názov"), max_length=256)
    date = forms.DateField(label=_("Dátum"), widget=forms.DateInput(format = '%d.%m.%Y'), input_formats=('%d.%m.%Y',))
