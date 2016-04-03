from django.utils.translation import ugettext as _
from django import forms

class SearchForm(forms.Form):
    name = forms.CharField(label=_("Názov materiálu"), max_length=80, required=False)





