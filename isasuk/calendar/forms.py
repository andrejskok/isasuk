from django.utils.translation import ugettext as _
from django import forms

class AddEventForm(forms.Form):
    title =  forms.CharField(label=_("Názov"), max_length=80)
    date = forms.DateTimeField(
      label=_("Dátum"),
      widget=forms.DateTimeInput(
        attrs={'id': 'datetimepicker'},
        format = '%d/%m/%Y %H:%M'),
      input_formats=('%d/%m/%Y %H:%M',))
